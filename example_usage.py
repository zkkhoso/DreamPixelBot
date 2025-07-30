#!/usr/bin/env python3
"""
Example usage of the Bulk Image Generator
This script demonstrates how to use the generator programmatically.
"""

import asyncio
import json
from bulk_image_generator import BulkImageGenerator, GenerationConfig, ImageRequest

async def example_basic_usage():
    """Basic example of generating a few images."""
    print("=== Basic Usage Example ===")
    
    # Configuration
    config = GenerationConfig(
        api_key="your_flux_api_key_here",  # Replace with your actual API key
        max_concurrent=3,
        output_dir="example_output"
    )
    
    # Create generator
    generator = BulkImageGenerator(config)
    
    # Create requests manually
    requests = [
        ImageRequest(
            prompt="a beautiful sunset over mountains",
            style="photorealistic",
            size="1024x1024",
            aspect_ratio="1:1",
            quality="standard",
            output_format="png"
        ),
        ImageRequest(
            prompt="a cute cat in anime style",
            style="anime style",
            size="1024x1408",
            aspect_ratio="3:4",
            quality="standard",
            output_format="png"
        ),
        ImageRequest(
            prompt="a futuristic cityscape at night",
            style="cyberpunk art",
            size="1792x1024",
            aspect_ratio="16:9",
            quality="hd",
            output_format="png"
        )
    ]
    
    # Generate images
    results = await generator.generate_bulk_images(requests)
    
    # Print results
    for i, result in enumerate(results):
        if "error" not in result:
            print(f"✓ Image {i+1}: {result.get('local_filepath', 'Unknown')}")
        else:
            print(f"✗ Image {i+1}: {result['error']}")

async def example_template_usage():
    """Example using the template system for multiple variations."""
    print("\n=== Template Usage Example ===")
    
    # Configuration
    config = GenerationConfig(
        api_key="your_flux_api_key_here",  # Replace with your actual API key
        max_concurrent=2,
        output_dir="template_example"
    )
    
    # Create generator
    generator = BulkImageGenerator(config)
    
    # Create requests using template
    requests = generator.create_requests_from_template(
        base_prompt="a majestic dragon",
        variations=["flying over mountains", "in a cave", "breathing fire"],
        styles=["realistic", "anime"],
        sizes=["square", "portrait"],
        qualities=["standard"]
    )
    
    print(f"Will generate {len(requests)} images using template system")
    
    # Generate images
    results = await generator.generate_bulk_images(requests)
    
    # Summary
    successful = sum(1 for r in results if "error" not in r)
    print(f"Successfully generated {successful}/{len(requests)} images")

async def example_with_config_file():
    """Example using a configuration file."""
    print("\n=== Configuration File Example ===")
    
    # Create a sample config file
    config_data = {
        "api_key": "your_flux_api_key_here",  # Replace with your actual API key
        "max_concurrent": 2,
        "output_dir": "config_example",
        "save_metadata": True,
        "retry_attempts": 3,
        "retry_delay": 1.5
    }
    
    with open("example_config.json", "w") as f:
        json.dump(config_data, f, indent=2)
    
    # Load configuration
    config = GenerationConfig(**config_data)
    generator = BulkImageGenerator(config)
    
    # Create simple requests
    requests = generator.create_requests_from_template(
        base_prompt="a peaceful forest scene",
        styles=["oil_painting", "watercolor"],
        sizes=["landscape"],
        qualities=["standard"]
    )
    
    print(f"Generating {len(requests)} forest scenes...")
    results = await generator.generate_bulk_images(requests)
    
    successful = sum(1 for r in results if "error" not in r)
    print(f"Successfully generated {successful}/{len(requests)} images")

async def main():
    """Run all examples."""
    print("Bulk Image Generator - Example Usage")
    print("=" * 50)
    print("Note: Replace 'your_flux_api_key_here' with your actual Flux API key")
    print()
    
    try:
        # Run examples (commented out to avoid actual API calls)
        print("Examples are ready to run. Uncomment the lines below to execute:")
        print()
        
        # await example_basic_usage()
        # await example_template_usage()
        # await example_with_config_file()
        
        print("To run examples:")
        print("1. Replace 'your_flux_api_key_here' with your actual API key")
        print("2. Uncomment the example function calls above")
        print("3. Run: python example_usage.py")
        
    except Exception as e:
        print(f"Error running examples: {e}")

if __name__ == "__main__":
    asyncio.run(main())