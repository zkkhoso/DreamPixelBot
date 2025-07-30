#!/usr/bin/env python3
"""
Test script to verify the bulk image generator setup
"""

import sys
import importlib

def test_imports():
    """Test if all required modules can be imported."""
    print("Testing imports...")
    
    required_modules = [
        'asyncio',
        'aiohttp',
        'aiofiles',
        'json',
        'pathlib',
        'argparse',
        'dataclasses'
    ]
    
    failed_imports = []
    
    for module in required_modules:
        try:
            importlib.import_module(module)
            print(f"✓ {module}")
        except ImportError as e:
            print(f"✗ {module}: {e}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\nFailed to import: {', '.join(failed_imports)}")
        print("Please install missing dependencies:")
        print("pip install -r requirements.txt")
        return False
    
    print("\nAll imports successful!")
    return True

def test_bulk_generator_import():
    """Test if the bulk image generator can be imported."""
    print("\nTesting bulk image generator import...")
    
    try:
        from bulk_image_generator import BulkImageGenerator, GenerationConfig, ImageRequest
        print("✓ Bulk image generator classes imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Failed to import bulk image generator: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error importing bulk image generator: {e}")
        return False

def test_config_creation():
    """Test if configuration objects can be created."""
    print("\nTesting configuration creation...")
    
    try:
        from bulk_image_generator import GenerationConfig, ImageRequest
        
        # Test GenerationConfig
        config = GenerationConfig(api_key="test_key")
        print("✓ GenerationConfig created successfully")
        
        # Test ImageRequest
        request = ImageRequest(
            prompt="test prompt",
            style="test style",
            size="1024x1024",
            aspect_ratio="1:1",
            quality="standard",
            output_format="png"
        )
        print("✓ ImageRequest created successfully")
        
        return True
    except Exception as e:
        print(f"✗ Failed to create configuration objects: {e}")
        return False

def test_generator_initialization():
    """Test if the generator can be initialized."""
    print("\nTesting generator initialization...")
    
    try:
        from bulk_image_generator import BulkImageGenerator, GenerationConfig
        
        config = GenerationConfig(
            api_key="test_key",
            output_dir="test_output"
        )
        
        generator = BulkImageGenerator(config)
        print("✓ BulkImageGenerator initialized successfully")
        
        # Test available options
        print(f"  Available styles: {len(generator.styles)}")
        print(f"  Available sizes: {len(generator.sizes)}")
        print(f"  Available qualities: {len(generator.qualities)}")
        print(f"  Available formats: {len(generator.formats)}")
        
        return True
    except Exception as e:
        print(f"✗ Failed to initialize generator: {e}")
        return False

def main():
    """Run all tests."""
    print("Bulk Image Generator - Setup Test")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_bulk_generator_import,
        test_config_creation,
        test_generator_initialization
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n{'='*40}")
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your setup is ready.")
        print("\nNext steps:")
        print("1. Get your Flux API key")
        print("2. Run: python bulk_image_generator.py")
        print("3. Or use command line: python bulk_image_generator.py --help")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("\nTroubleshooting:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Check Python version (3.7+ required)")
        print("3. Verify all files are in the same directory")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)