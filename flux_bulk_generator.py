#!/usr/bin/env python3
"""
Flux Bulk Images Generator Tool

A comprehensive tool for generating multiple images in bulk using various Flux API providers.
Supports Black Forest Labs, DeepInfra, Leonardo AI, Replicate, and Astria APIs.
"""

import os
import json
import time
import base64
import asyncio
import aiohttp
import argparse
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
from datetime import datetime
import logging
from tqdm.asyncio import tqdm
import yaml

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('flux_generator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class ImageRequest:
    """Individual image generation request"""
    prompt: str
    size: str = "1024x1024"
    style: str = "dynamic"
    quality: str = "standard"
    seed: Optional[int] = None
    output_filename: Optional[str] = None

@dataclass
class ProviderConfig:
    """Configuration for different API providers"""
    name: str
    api_key: str
    base_url: str
    model_id: str
    headers: Dict[str, str]
    max_concurrent: int = 3
    retry_attempts: int = 3
    retry_delay: float = 1.0

class FluxProvider:
    """Base class for Flux API providers"""
    
    def __init__(self, config: ProviderConfig):
        self.config = config
        self.session: Optional[aiohttp.ClientSession] = None
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            headers=self.config.headers,
            timeout=aiohttp.ClientTimeout(total=120)
        )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def generate_image(self, request: ImageRequest) -> Dict[str, Any]:
        """Generate a single image - to be implemented by subclasses"""
        raise NotImplementedError

class BlackForestLabsProvider(FluxProvider):
    """Black Forest Labs API provider"""
    
    async def generate_image(self, request: ImageRequest) -> Dict[str, Any]:
        data = {
            "prompt": request.prompt,
            "width": int(request.size.split('x')[0]),
            "height": int(request.size.split('x')[1]),
        }
        
        if request.seed:
            data["seed"] = request.seed
            
        async with self.session.post(
            f"{self.config.base_url}/v1/flux-pro-1.1",
            json=data
        ) as response:
            if response.status == 200:
                result = await response.json()
                return {
                    "success": True,
                    "image_data": result.get("result", {}).get("sample"),
                    "provider": "black-forest-labs"
                }
            else:
                error_text = await response.text()
                return {
                    "success": False,
                    "error": f"HTTP {response.status}: {error_text}",
                    "provider": "black-forest-labs"
                }

class DeepInfraProvider(FluxProvider):
    """DeepInfra API provider"""
    
    async def generate_image(self, request: ImageRequest) -> Dict[str, Any]:
        data = {
            "prompt": request.prompt,
            "size": request.size,
            "model": self.config.model_id,
            "n": 1,
            "response_format": "b64_json"
        }
        
        async with self.session.post(
            f"{self.config.base_url}/v1/openai/images/generations",
            json=data
        ) as response:
            if response.status == 200:
                result = await response.json()
                return {
                    "success": True,
                    "image_data": result["data"][0]["b64_json"],
                    "provider": "deepinfra"
                }
            else:
                error_text = await response.text()
                return {
                    "success": False,
                    "error": f"HTTP {response.status}: {error_text}",
                    "provider": "deepinfra"
                }

class LeonardoAIProvider(FluxProvider):
    """Leonardo AI API provider"""
    
    async def generate_image(self, request: ImageRequest) -> Dict[str, Any]:
        style_map = {
            "dynamic": "111dc692-d470-4eec-b791-3475abac4c46",
            "creative": "6fedbf1f-4a17-45ec-84fb-92fe524a29ef",
            "portrait": "8e2bc543-6ee2-45f9-bcd9-594b6ce84dcd",
            "3d": "debdf72a-91a4-467b-bf61-cc02bdeb69c6",
            "anime": "b2a54a51-230b-4d4f-ad4e-8409bf58645f"
        }
        
        data = {
            "modelId": self.config.model_id,
            "prompt": request.prompt,
            "num_images": 1,
            "width": int(request.size.split('x')[0]),
            "height": int(request.size.split('x')[1]),
            "contrast": 3.5,
            "styleUUID": style_map.get(request.style, style_map["dynamic"]),
            "enhancePrompt": False
        }
        
        if request.seed:
            data["seed"] = request.seed
            
        async with self.session.post(
            f"{self.config.base_url}/api/rest/v1/generations",
            json=data
        ) as response:
            if response.status == 200:
                result = await response.json()
                generation_id = result.get("sdGenerationJob", {}).get("generationId")
                
                # Poll for completion
                return await self._poll_leonardo_result(generation_id)
            else:
                error_text = await response.text()
                return {
                    "success": False,
                    "error": f"HTTP {response.status}: {error_text}",
                    "provider": "leonardo"
                }
    
    async def _poll_leonardo_result(self, generation_id: str) -> Dict[str, Any]:
        """Poll Leonardo AI for generation completion"""
        max_polls = 60
        poll_interval = 2
        
        for _ in range(max_polls):
            async with self.session.get(
                f"{self.config.base_url}/api/rest/v1/generations/{generation_id}"
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    generation = result.get("generations_by_pk", {})
                    status = generation.get("status")
                    
                    if status == "COMPLETE":
                        images = generation.get("generated_images", [])
                        if images:
                            return {
                                "success": True,
                                "image_data": images[0].get("url"),
                                "provider": "leonardo"
                            }
                    elif status == "FAILED":
                        return {
                            "success": False,
                            "error": "Generation failed",
                            "provider": "leonardo"
                        }
                    
                    await asyncio.sleep(poll_interval)
                    
        return {
            "success": False,
            "error": "Timeout waiting for generation",
            "provider": "leonardo"
        }

class ReplicateProvider(FluxProvider):
    """Replicate API provider"""
    
    async def generate_image(self, request: ImageRequest) -> Dict[str, Any]:
        data = {
            "input": {
                "prompt": request.prompt,
                "width": int(request.size.split('x')[0]),
                "height": int(request.size.split('x')[1]),
                "num_outputs": 1,
                "output_format": "png",
                "output_quality": 90
            }
        }
        
        if request.seed:
            data["input"]["seed"] = request.seed
            
        async with self.session.post(
            f"{self.config.base_url}/v1/predictions",
            json={
                "version": self.config.model_id,
                **data
            }
        ) as response:
            if response.status == 201:
                result = await response.json()
                prediction_id = result.get("id")
                
                # Poll for completion
                return await self._poll_replicate_result(prediction_id)
            else:
                error_text = await response.text()
                return {
                    "success": False,
                    "error": f"HTTP {response.status}: {error_text}",
                    "provider": "replicate"
                }
    
    async def _poll_replicate_result(self, prediction_id: str) -> Dict[str, Any]:
        """Poll Replicate for prediction completion"""
        max_polls = 60
        poll_interval = 2
        
        for _ in range(max_polls):
            async with self.session.get(
                f"{self.config.base_url}/v1/predictions/{prediction_id}"
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    status = result.get("status")
                    
                    if status == "succeeded":
                        output = result.get("output", [])
                        if output:
                            return {
                                "success": True,
                                "image_data": output[0],
                                "provider": "replicate"
                            }
                    elif status == "failed":
                        return {
                            "success": False,
                            "error": result.get("error", "Generation failed"),
                            "provider": "replicate"
                        }
                    
                    await asyncio.sleep(poll_interval)
                    
        return {
            "success": False,
            "error": "Timeout waiting for prediction",
            "provider": "replicate"
        }

class FluxBulkGenerator:
    """Main bulk image generator class"""
    
    def __init__(self, config_path: str = "flux_config.yaml"):
        self.config_path = config_path
        self.providers: Dict[str, FluxProvider] = {}
        self.output_dir = Path("generated_images")
        self.output_dir.mkdir(exist_ok=True)
        
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.error(f"Configuration file {self.config_path} not found")
            return {}
    
    def create_providers(self, config: Dict[str, Any]) -> None:
        """Create API provider instances"""
        provider_configs = config.get("providers", {})
        
        for provider_name, provider_config in provider_configs.items():
            if not provider_config.get("enabled", False):
                continue
                
            api_key = provider_config.get("api_key") or os.getenv(provider_config.get("api_key_env", ""))
            if not api_key:
                logger.warning(f"No API key found for {provider_name}")
                continue
            
            config_obj = ProviderConfig(
                name=provider_name,
                api_key=api_key,
                base_url=provider_config["base_url"],
                model_id=provider_config["model_id"],
                headers={"Authorization": f"Bearer {api_key}"},
                max_concurrent=provider_config.get("max_concurrent", 3),
                retry_attempts=provider_config.get("retry_attempts", 3),
                retry_delay=provider_config.get("retry_delay", 1.0)
            )
            
            if provider_name == "black_forest_labs":
                self.providers[provider_name] = BlackForestLabsProvider(config_obj)
            elif provider_name == "deepinfra":
                self.providers[provider_name] = DeepInfraProvider(config_obj)
            elif provider_name == "leonardo":
                self.providers[provider_name] = LeonardoAIProvider(config_obj)
            elif provider_name == "replicate":
                self.providers[provider_name] = ReplicateProvider(config_obj)
    
    async def generate_single_image(self, provider: FluxProvider, request: ImageRequest, semaphore: asyncio.Semaphore, progress_bar) -> Dict[str, Any]:
        """Generate a single image with retry logic"""
        async with semaphore:
            for attempt in range(provider.config.retry_attempts):
                try:
                    result = await provider.generate_image(request)
                    if result["success"]:
                        # Save image
                        filename = request.output_filename or f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{result['provider']}.png"
                        filepath = self.output_dir / filename
                        
                        if result["image_data"].startswith("http"):
                            # URL - download the image
                            async with provider.session.get(result["image_data"]) as img_response:
                                if img_response.status == 200:
                                    with open(filepath, 'wb') as f:
                                        f.write(await img_response.read())
                        else:
                            # Base64 data
                            image_data = base64.b64decode(result["image_data"])
                            with open(filepath, 'wb') as f:
                                f.write(image_data)
                        
                        result["filepath"] = str(filepath)
                        result["prompt"] = request.prompt
                        progress_bar.update(1)
                        return result
                    else:
                        if attempt == provider.config.retry_attempts - 1:
                            progress_bar.update(1)
                            return result
                        await asyncio.sleep(provider.config.retry_delay * (2 ** attempt))
                        
                except Exception as e:
                    logger.error(f"Error generating image: {e}")
                    if attempt == provider.config.retry_attempts - 1:
                        progress_bar.update(1)
                        return {
                            "success": False,
                            "error": str(e),
                            "provider": provider.config.name,
                            "prompt": request.prompt
                        }
                    await asyncio.sleep(provider.config.retry_delay * (2 ** attempt))
    
    async def generate_bulk_images(self, requests: List[ImageRequest], provider_name: str = None) -> List[Dict[str, Any]]:
        """Generate multiple images in bulk"""
        if not self.providers:
            raise ValueError("No providers configured")
        
        if provider_name and provider_name not in self.providers:
            raise ValueError(f"Provider {provider_name} not found")
        
        provider = self.providers[provider_name] if provider_name else list(self.providers.values())[0]
        
        logger.info(f"Starting bulk generation of {len(requests)} images using {provider.config.name}")
        
        async with provider:
            semaphore = asyncio.Semaphore(provider.config.max_concurrent)
            
            with tqdm(total=len(requests), desc="Generating images") as progress_bar:
                tasks = [
                    self.generate_single_image(provider, request, semaphore, progress_bar)
                    for request in requests
                ]
                
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
        # Process results and log summary
        successful = sum(1 for r in results if isinstance(r, dict) and r.get("success"))
        failed = len(results) - successful
        
        logger.info(f"Generation complete: {successful} successful, {failed} failed")
        
        # Save results to JSON
        results_file = self.output_dir / f"results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(results_file, 'w') as f:
            json.dump([r for r in results if isinstance(r, dict)], f, indent=2)
        
        return results
    
    def load_prompts_from_file(self, file_path: str) -> List[ImageRequest]:
        """Load prompts from various file formats"""
        path = Path(file_path)
        
        if path.suffix.lower() == '.json':
            with open(path, 'r') as f:
                data = json.load(f)
                if isinstance(data, list):
                    return [ImageRequest(**item) if isinstance(item, dict) else ImageRequest(prompt=str(item)) for item in data]
                else:
                    return [ImageRequest(**data)]
        
        elif path.suffix.lower() in ['.yaml', '.yml']:
            with open(path, 'r') as f:
                data = yaml.safe_load(f)
                if isinstance(data, list):
                    return [ImageRequest(**item) if isinstance(item, dict) else ImageRequest(prompt=str(item)) for item in data]
                else:
                    return [ImageRequest(**data)]
        
        elif path.suffix.lower() == '.txt':
            with open(path, 'r') as f:
                prompts = [line.strip() for line in f if line.strip()]
                return [ImageRequest(prompt=prompt) for prompt in prompts]
        
        else:
            raise ValueError(f"Unsupported file format: {path.suffix}")

def create_sample_config():
    """Create a sample configuration file"""
    config = {
        "providers": {
            "black_forest_labs": {
                "enabled": False,
                "api_key_env": "BFL_API_KEY",
                "base_url": "https://api.bfl.ml",
                "model_id": "flux-pro-1.1",
                "max_concurrent": 3,
                "retry_attempts": 3,
                "retry_delay": 1.0
            },
            "deepinfra": {
                "enabled": False,
                "api_key_env": "DEEPINFRA_API_KEY",
                "base_url": "https://api.deepinfra.com",
                "model_id": "black-forest-labs/FLUX-1.1-pro",
                "max_concurrent": 5,
                "retry_attempts": 3,
                "retry_delay": 1.0
            },
            "leonardo": {
                "enabled": False,
                "api_key_env": "LEONARDO_API_KEY",
                "base_url": "https://cloud.leonardo.ai",
                "model_id": "b2614463-296c-462a-9586-aafdb8f00e36",
                "max_concurrent": 3,
                "retry_attempts": 3,
                "retry_delay": 2.0
            },
            "replicate": {
                "enabled": False,
                "api_key_env": "REPLICATE_API_TOKEN",
                "base_url": "https://api.replicate.com",
                "model_id": "black-forest-labs/flux-pro",
                "max_concurrent": 3,
                "retry_attempts": 3,
                "retry_delay": 1.0
            }
        },
        "default_settings": {
            "size": "1024x1024",
            "style": "dynamic",
            "quality": "standard",
            "output_format": "png"
        }
    }
    
    with open("flux_config.yaml", 'w') as f:
        yaml.dump(config, f, default_flow_style=False, indent=2)
    
    print("Sample configuration file 'flux_config.yaml' created!")
    print("Please edit it with your API keys and enable the providers you want to use.")

def create_sample_prompts():
    """Create sample prompt files"""
    # JSON format
    json_prompts = [
        {
            "prompt": "A futuristic cityscape at sunset with flying cars",
            "size": "1024x1024",
            "style": "dynamic"
        },
        {
            "prompt": "A serene mountain landscape with a crystal clear lake",
            "size": "1024x1024",
            "style": "creative"
        },
        {
            "prompt": "A portrait of a wise old wizard with a long beard",
            "size": "1024x1024",
            "style": "portrait"
        }
    ]
    
    with open("sample_prompts.json", 'w') as f:
        json.dump(json_prompts, f, indent=2)
    
    # Text format
    text_prompts = [
        "A magical forest with glowing mushrooms and fireflies",
        "A steampunk robot in a Victorian laboratory",
        "An underwater city with bioluminescent architecture",
        "A space station orbiting a colorful nebula",
        "A cozy cabin in the woods during autumn"
    ]
    
    with open("sample_prompts.txt", 'w') as f:
        f.write('\n'.join(text_prompts))
    
    print("Sample prompt files created: 'sample_prompts.json' and 'sample_prompts.txt'")

async def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description="Flux Bulk Image Generator")
    parser.add_argument("--config", default="flux_config.yaml", help="Configuration file path")
    parser.add_argument("--prompts", help="Prompts file path (JSON, YAML, or TXT)")
    parser.add_argument("--prompt", help="Single prompt to generate")
    parser.add_argument("--provider", help="Specific provider to use")
    parser.add_argument("--size", default="1024x1024", help="Image size")
    parser.add_argument("--style", default="dynamic", help="Image style")
    parser.add_argument("--count", type=int, default=1, help="Number of images to generate (for single prompt)")
    parser.add_argument("--output-dir", help="Output directory for generated images")
    parser.add_argument("--create-config", action="store_true", help="Create sample configuration file")
    parser.add_argument("--create-samples", action="store_true", help="Create sample prompt files")
    
    args = parser.parse_args()
    
    if args.create_config:
        create_sample_config()
        return
    
    if args.create_samples:
        create_sample_prompts()
        return
    
    generator = FluxBulkGenerator(args.config)
    
    if args.output_dir:
        generator.output_dir = Path(args.output_dir)
        generator.output_dir.mkdir(exist_ok=True)
    
    config = generator.load_config()
    if not config:
        print("No configuration found. Use --create-config to create a sample configuration.")
        return
    
    generator.create_providers(config)
    
    if not generator.providers:
        print("No providers configured or enabled. Please check your configuration.")
        return
    
    requests = []
    
    if args.prompts:
        requests = generator.load_prompts_from_file(args.prompts)
    elif args.prompt:
        for i in range(args.count):
            filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{i+1}.png" if args.count > 1 else None
            requests.append(ImageRequest(
                prompt=args.prompt,
                size=args.size,
                style=args.style,
                output_filename=filename
            ))
    else:
        print("Please provide either --prompts file or --prompt text")
        return
    
    try:
        results = await generator.generate_bulk_images(requests, args.provider)
        
        print(f"\nGeneration Summary:")
        print(f"Total requests: {len(requests)}")
        print(f"Successful: {sum(1 for r in results if r.get('success'))}")
        print(f"Failed: {sum(1 for r in results if not r.get('success'))}")
        print(f"Output directory: {generator.output_dir}")
        
    except Exception as e:
        logger.error(f"Error during bulk generation: {e}")
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())