#!/usr/bin/env python3
"""
Bulk Image Generator using Flux API
A powerful tool for generating multiple images with various styles and configurations.
"""

import os
import json
import asyncio
import aiohttp
import aiofiles
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Union
import argparse
import sys
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor
import time

@dataclass
class ImageRequest:
    """Represents a single image generation request."""
    prompt: str
    style: str
    size: str
    aspect_ratio: str
    quality: str
    output_format: str
    seed: Optional[int] = None

@dataclass
class GenerationConfig:
    """Configuration for bulk image generation."""
    api_key: str
    base_url: str = "https://api.flux.ai/v1"
    max_concurrent: int = 5
    output_dir: str = "generated_images"
    save_metadata: bool = True
    retry_attempts: int = 3
    retry_delay: float = 2.0

class FluxAPIClient:
    """Client for interacting with Flux API."""
    
    def __init__(self, config: GenerationConfig):
        self.config = config
        self.session = None
        self.headers = {
            "Authorization": f"Bearer {config.api_key}",
            "Content-Type": "application/json"
        }
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers=self.headers)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def generate_image(self, request: ImageRequest) -> Dict:
        """Generate a single image using Flux API."""
        payload = {
            "prompt": request.prompt,
            "style": request.style,
            "size": request.size,
            "aspect_ratio": request.aspect_ratio,
            "quality": request.quality,
            "output_format": request.output_format
        }
        
        if request.seed is not None:
            payload["seed"] = request.seed
        
        for attempt in range(self.config.retry_attempts):
            try:
                async with self.session.post(
                    f"{self.config.base_url}/images/generations",
                    json=payload
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    elif response.status == 429:
                        wait_time = (attempt + 1) * self.config.retry_delay
                        print(f"Rate limited. Waiting {wait_time}s before retry...")
                        await asyncio.sleep(wait_time)
                    else:
                        error_text = await response.text()
                        raise Exception(f"API Error {response.status}: {error_text}")
            except Exception as e:
                if attempt == self.config.retry_attempts - 1:
                    raise e
                await asyncio.sleep(self.config.retry_delay)
        
        raise Exception("Max retry attempts exceeded")

class BulkImageGenerator:
    """Main class for bulk image generation."""
    
    def __init__(self, config: GenerationConfig):
        self.config = config
        self.output_path = Path(config.output_dir)
        self.output_path.mkdir(exist_ok=True)
        
        # Predefined styles and configurations
        self.styles = {
            "realistic": "photorealistic",
            "anime": "anime style",
            "cyberpunk": "cyberpunk art",
            "oil_painting": "oil painting",
            "watercolor": "watercolor painting",
            "sketch": "pencil sketch",
            "digital_art": "digital art",
            "vintage": "vintage style",
            "futuristic": "futuristic",
            "minimalist": "minimalist"
        }
        
        self.sizes = {
            "square": "1024x1024",
            "portrait": "1024x1408",
            "landscape": "1408x1024",
            "wide": "1792x1024",
            "tall": "1024x1792"
        }
        
        self.qualities = ["standard", "hd"]
        self.formats = ["png", "jpeg", "webp"]
    
    async def download_image(self, url: str, filename: str) -> str:
        """Download image from URL and save to local file."""
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    filepath = self.output_path / filename
                    async with aiofiles.open(filepath, 'wb') as f:
                        await f.write(await response.read())
                    return str(filepath)
                else:
                    raise Exception(f"Failed to download image: {response.status}")
    
    async def save_metadata(self, requests: List[ImageRequest], results: List[Dict]):
        """Save metadata about the generation process."""
        if not self.config.save_metadata:
            return
        
        metadata = {
            "generation_time": datetime.now().isoformat(),
            "total_images": len(requests),
            "config": {
                "max_concurrent": self.config.max_concurrent,
                "output_dir": str(self.output_path),
                "retry_attempts": self.config.retry_attempts
            },
            "requests": [
                {
                    "prompt": req.prompt,
                    "style": req.style,
                    "size": req.size,
                    "aspect_ratio": req.aspect_ratio,
                    "quality": req.quality,
                    "output_format": req.output_format,
                    "seed": req.seed
                }
                for req in requests
            ],
            "results": results
        }
        
        metadata_file = self.output_path / f"metadata_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        async with aiofiles.open(metadata_file, 'w') as f:
            await f.write(json.dumps(metadata, indent=2))
    
    async def generate_bulk_images(self, requests: List[ImageRequest]) -> List[Dict]:
        """Generate multiple images concurrently."""
        print(f"Starting bulk generation of {len(requests)} images...")
        print(f"Using {self.config.max_concurrent} concurrent requests")
        
        semaphore = asyncio.Semaphore(self.config.max_concurrent)
        results = []
        
        async def process_single_request(request: ImageRequest, index: int) -> Dict:
            async with semaphore:
                try:
                    print(f"Generating image {index + 1}/{len(requests)}: {request.prompt[:50]}...")
                    
                    async with FluxAPIClient(self.config) as client:
                        result = await client.generate_image(request)
                    
                    # Download the image
                    if "data" in result and len(result["data"]) > 0:
                        image_url = result["data"][0]["url"]
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"image_{index + 1:03d}_{timestamp}.{request.output_format}"
                        filepath = await self.download_image(image_url, filename)
                        
                        result["local_filepath"] = filepath
                        print(f"✓ Generated: {filename}")
                    else:
                        print(f"✗ Failed: No image data in response")
                    
                    return result
                    
                except Exception as e:
                    error_result = {
                        "error": str(e),
                        "request": {
                            "prompt": request.prompt,
                            "style": request.style,
                            "size": request.size
                        },
                        "index": index
                    }
                    print(f"✗ Error generating image {index + 1}: {e}")
                    return error_result
        
        # Create tasks for all requests
        tasks = [
            process_single_request(request, i) 
            for i, request in enumerate(requests)
        ]
        
        # Execute all tasks concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Save metadata
        await self.save_metadata(requests, results)
        
        return results
    
    def create_requests_from_template(self, base_prompt: str, variations: List[str] = None,
                                    styles: List[str] = None, sizes: List[str] = None,
                                    qualities: List[str] = None) -> List[ImageRequest]:
        """Create multiple requests from a template with variations."""
        if variations is None:
            variations = [base_prompt]
        
        if styles is None:
            styles = ["realistic"]
        
        if sizes is None:
            sizes = ["square"]
        
        if qualities is None:
            qualities = ["standard"]
        
        requests = []
        
        for variation in variations:
            for style in styles:
                for size in sizes:
                    for quality in qualities:
                        request = ImageRequest(
                            prompt=f"{base_prompt} {variation}",
                            style=self.styles.get(style, style),
                            size=self.sizes.get(size, size),
                            aspect_ratio="1:1" if size == "square" else "16:9",
                            quality=quality,
                            output_format="png"
                        )
                        requests.append(request)
        
        return requests

def print_available_options(generator: BulkImageGenerator):
    """Print available styles, sizes, and options."""
    print("\n=== Available Options ===")
    
    print("\nStyles:")
    for key, value in generator.styles.items():
        print(f"  {key}: {value}")
    
    print("\nSizes:")
    for key, value in generator.sizes.items():
        print(f"  {key}: {value}")
    
    print("\nQualities:")
    for quality in generator.qualities:
        print(f"  {quality}")
    
    print("\nFormats:")
    for format_type in generator.formats:
        print(f"  {format_type}")

async def main():
    """Main function with command-line interface."""
    parser = argparse.ArgumentParser(description="Bulk Image Generator using Flux API")
    parser.add_argument("--api-key", help="Flux API key")
    parser.add_argument("--prompt", help="Base prompt for image generation")
    parser.add_argument("--variations", nargs="+", help="Prompt variations")
    parser.add_argument("--styles", nargs="+", help="Image styles to use")
    parser.add_argument("--sizes", nargs="+", help="Image sizes to generate")
    parser.add_argument("--qualities", nargs="+", help="Image qualities")
    parser.add_argument("--output-dir", default="generated_images", help="Output directory")
    parser.add_argument("--max-concurrent", type=int, default=5, help="Max concurrent requests")
    parser.add_argument("--list-options", action="store_true", help="List available options")
    parser.add_argument("--config-file", help="JSON configuration file")
    
    args = parser.parse_args()
    
    # Handle list-options case first
    if args.list_options:
        config = GenerationConfig(api_key="dummy")  # Dummy config for listing options
        generator = BulkImageGenerator(config)
        print_available_options(generator)
        return
    
    # Check required arguments for generation
    if not args.api_key:
        parser.error("--api-key is required for image generation")
    if not args.prompt:
        parser.error("--prompt is required for image generation")
    
    # Load configuration from file if provided
    if args.config_file:
        with open(args.config_file, 'r') as f:
            config_data = json.load(f)
            config = GenerationConfig(**config_data)
    else:
        config = GenerationConfig(
            api_key=args.api_key,
            output_dir=args.output_dir,
            max_concurrent=args.max_concurrent
        )
    
    generator = BulkImageGenerator(config)
    
    if args.list_options:
        print_available_options(generator)
        return
    
    # Create requests
    requests = generator.create_requests_from_template(
        base_prompt=args.prompt,
        variations=args.variations,
        styles=args.styles,
        sizes=args.sizes,
        qualities=args.qualities
    )
    
    if not requests:
        print("No requests to process. Check your arguments.")
        return
    
    print(f"Will generate {len(requests)} images:")
    for i, req in enumerate(requests[:5]):  # Show first 5
        print(f"  {i+1}. {req.prompt} ({req.style}, {req.size})")
    if len(requests) > 5:
        print(f"  ... and {len(requests) - 5} more")
    
    # Confirm before proceeding
    response = input("\nProceed with generation? (y/N): ")
    if response.lower() != 'y':
        print("Generation cancelled.")
        return
    
    # Generate images
    start_time = time.time()
    results = await generator.generate_bulk_images(requests)
    end_time = time.time()
    
    # Print summary
    successful = sum(1 for r in results if "error" not in r)
    failed = len(results) - successful
    
    print(f"\n=== Generation Complete ===")
    print(f"Total time: {end_time - start_time:.2f} seconds")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Output directory: {config.output_dir}")
    
    if failed > 0:
        print("\nFailed generations:")
        for result in results:
            if "error" in result:
                print(f"  - {result['request']['prompt']}: {result['error']}")

if __name__ == "__main__":
    # Check if running in interactive mode
    if len(sys.argv) == 1:
        print("Bulk Image Generator - Interactive Mode")
        print("=" * 40)
        
        api_key = input("Enter your Flux API key: ").strip()
        if not api_key:
            print("API key is required!")
            sys.exit(1)
        
        prompt = input("Enter base prompt: ").strip()
        if not prompt:
            print("Prompt is required!")
            sys.exit(1)
        
        print("\nAvailable styles: realistic, anime, cyberpunk, oil_painting, watercolor, sketch, digital_art, vintage, futuristic, minimalist")
        styles_input = input("Enter styles (comma-separated, or press Enter for realistic): ").strip()
        styles = [s.strip() for s in styles_input.split(",")] if styles_input else ["realistic"]
        
        print("\nAvailable sizes: square, portrait, landscape, wide, tall")
        sizes_input = input("Enter sizes (comma-separated, or press Enter for square): ").strip()
        sizes = [s.strip() for s in sizes_input.split(",")] if sizes_input else ["square"]
        
        variations_input = input("Enter prompt variations (comma-separated, or press Enter for none): ").strip()
        variations = [v.strip() for v in variations_input.split(",")] if variations_input else None
        
        # Set up sys.argv for argparse
        sys.argv = [
            "bulk_image_generator.py",
            "--api-key", api_key,
            "--prompt", prompt,
            "--styles"
        ] + styles + ["--sizes"] + sizes
        
        if variations:
            sys.argv.extend(["--variations"] + variations)
    
    asyncio.run(main())