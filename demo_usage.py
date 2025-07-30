#!/usr/bin/env python3
"""
Demo script showing how to use the Flux Bulk Generator programmatically
"""

import asyncio
import os
from flux_bulk_generator import FluxBulkGenerator, ImageRequest

async def demo_basic_usage():
    """Basic usage example"""
    print("=== Basic Usage Demo ===")
    
    # Create generator instance
    generator = FluxBulkGenerator("flux_config.yaml")
    
    # Load configuration
    config = generator.load_config()
    if not config:
        print("Please create configuration file first: python3 flux_bulk_generator.py --create-config")
        return
    
    generator.create_providers(config)
    
    if not generator.providers:
        print("No providers enabled. Please check your configuration and API keys.")
        return
    
    # Create some image requests
    requests = [
        ImageRequest(
            prompt="A beautiful sunset over mountains",
            size="1024x1024",
            style="dynamic"
        ),
        ImageRequest(
            prompt="A futuristic robot in a cyberpunk city",
            size="1024x1024",
            style="creative"
        ),
        ImageRequest(
            prompt="A peaceful forest with a hidden waterfall",
            size="1024x1024",
            style="dynamic"
        )
    ]
    
    try:
        # Generate images
        results = await generator.generate_bulk_images(requests)
        
        # Print results
        print(f"Generated {len(results)} images:")
        for i, result in enumerate(results):
            if result.get("success"):
                print(f"  ✅ Image {i+1}: {result.get('filepath')}")
            else:
                print(f"  ❌ Image {i+1} failed: {result.get('error')}")
                
    except Exception as e:
        print(f"Error: {e}")

async def demo_file_loading():
    """Demo loading prompts from files"""
    print("\n=== File Loading Demo ===")
    
    generator = FluxBulkGenerator()
    
    # Load from different file formats
    try:
        # Load from text file
        requests_txt = generator.load_prompts_from_file("sample_prompts.txt")
        print(f"Loaded {len(requests_txt)} prompts from TXT file")
        
        # Load from JSON file
        requests_json = generator.load_prompts_from_file("sample_prompts.json")
        print(f"Loaded {len(requests_json)} prompts from JSON file")
        
        # Show first request details
        if requests_json:
            req = requests_json[0]
            print(f"First JSON request: '{req.prompt}' ({req.size}, {req.style})")
            
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        print("Run: python3 flux_bulk_generator.py --create-samples")
    except Exception as e:
        print(f"Error loading files: {e}")

async def demo_custom_requests():
    """Demo creating custom image requests with different parameters"""
    print("\n=== Custom Requests Demo ===")
    
    # Create requests with different parameters
    custom_requests = [
        ImageRequest(
            prompt="A portrait of a wise old wizard",
            size="512x512",
            style="portrait",
            output_filename="wizard_portrait.png"
        ),
        ImageRequest(
            prompt="Abstract geometric patterns in bright colors",
            size="1024x1024",
            style="creative",
            seed=42,
            output_filename="abstract_art.png"
        ),
        ImageRequest(
            prompt="A 3D rendered spaceship in deep space",
            size="1024x1024",
            style="3d",
            output_filename="spaceship_3d.png"
        )
    ]
    
    print("Created custom requests:")
    for i, req in enumerate(custom_requests):
        print(f"  {i+1}. '{req.prompt}' -> {req.output_filename}")
        print(f"     Size: {req.size}, Style: {req.style}, Seed: {req.seed}")

def demo_configuration():
    """Demo configuration management"""
    print("\n=== Configuration Demo ===")
    
    # Show how to check configuration
    generator = FluxBulkGenerator()
    config = generator.load_config()
    
    if config:
        providers = config.get("providers", {})
        enabled_providers = [name for name, cfg in providers.items() if cfg.get("enabled")]
        
        print(f"Available providers: {list(providers.keys())}")
        print(f"Enabled providers: {enabled_providers}")
        
        # Show environment variables needed
        print("\nRequired environment variables:")
        for name, cfg in providers.items():
            if cfg.get("enabled"):
                env_var = cfg.get("api_key_env")
                is_set = "✅" if os.getenv(env_var) else "❌"
                print(f"  {is_set} {env_var}")
    else:
        print("No configuration found. Create one with:")
        print("python3 flux_bulk_generator.py --create-config")

async def demo_provider_selection():
    """Demo using specific providers"""
    print("\n=== Provider Selection Demo ===")
    
    generator = FluxBulkGenerator()
    config = generator.load_config()
    
    if not config:
        print("No configuration found.")
        return
    
    generator.create_providers(config)
    
    if generator.providers:
        print("Available providers:")
        for name, provider in generator.providers.items():
            print(f"  - {name}: {provider.config.base_url}")
            print(f"    Model: {provider.config.model_id}")
            print(f"    Max concurrent: {provider.config.max_concurrent}")
        
        # Example request
        request = ImageRequest(prompt="A test image for provider demo")
        
        # You could generate with specific provider like this:
        # results = await generator.generate_bulk_images([request], "deepinfra")
        print(f"\nYou can specify provider in generate_bulk_images()")
    else:
        print("No providers configured or API keys missing.")

async def demo_batch_processing():
    """Demo batch processing scenarios"""
    print("\n=== Batch Processing Demo ===")
    
    # Example: Generate variations of a base prompt
    base_prompt = "A magical landscape"
    variations = [
        "at sunrise with golden light",
        "at night with aurora borealis",
        "in autumn with colorful leaves",
        "covered in snow during winter",
        "with a rainbow after rain"
    ]
    
    batch_requests = []
    for i, variation in enumerate(variations):
        full_prompt = f"{base_prompt} {variation}"
        batch_requests.append(ImageRequest(
            prompt=full_prompt,
            output_filename=f"landscape_variation_{i+1}.png"
        ))
    
    print(f"Created batch of {len(batch_requests)} variations:")
    for req in batch_requests:
        print(f"  - {req.prompt}")
    
    print("\nThis batch could be processed with:")
    print("results = await generator.generate_bulk_images(batch_requests)")

def demo_cli_examples():
    """Show CLI usage examples"""
    print("\n=== CLI Usage Examples ===")
    
    cli_examples = [
        "# Generate from a prompt file",
        "python3 flux_bulk_generator.py --prompts my_prompts.txt",
        "",
        "# Generate single prompt with specific settings",
        "python3 flux_bulk_generator.py --prompt 'Abstract art' --size 512x512 --style creative",
        "",
        "# Generate multiple copies",
        "python3 flux_bulk_generator.py --prompt 'Portrait' --count 5",
        "",
        "# Use specific provider",
        "python3 flux_bulk_generator.py --prompts prompts.json --provider deepinfra",
        "",
        "# Custom output directory",
        "python3 flux_bulk_generator.py --prompt 'Artwork' --output-dir ./my_art",
        "",
        "# Create configuration and samples",
        "python3 flux_bulk_generator.py --create-config",
        "python3 flux_bulk_generator.py --create-samples"
    ]
    
    for example in cli_examples:
        print(example)

async def main():
    """Run all demos"""
    print("🎨 Flux Bulk Generator - Demo Script")
    print("=" * 50)
    
    # Configuration demo (always works)
    demo_configuration()
    
    # CLI examples (always works)
    demo_cli_examples()
    
    # File loading demo
    await demo_file_loading()
    
    # Custom requests demo
    await demo_custom_requests()
    
    # Provider selection demo
    await demo_provider_selection()
    
    # Batch processing demo
    await demo_batch_processing()
    
    # Only run actual generation if we have providers configured
    generator = FluxBulkGenerator()
    config = generator.load_config()
    if config:
        generator.create_providers(config)
        if generator.providers:
            print("\n⚠️  Would you like to run the actual image generation demo?")
            print("This will generate real images using your API keys.")
            response = input("Type 'yes' to continue: ").lower()
            if response == 'yes':
                await demo_basic_usage()
            else:
                print("Skipping actual generation demo.")
        else:
            print("\n⚠️  No providers configured. Set up API keys to run generation demos.")
    else:
        print("\n⚠️  No configuration found. Run --create-config first.")
    
    print("\n✨ Demo complete! Check the README.md for more details.")

if __name__ == "__main__":
    asyncio.run(main())