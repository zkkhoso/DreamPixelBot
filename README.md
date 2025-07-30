# Bulk Image Generator using Flux API

A powerful and efficient tool for generating multiple images using the Flux API. This tool supports concurrent generation, multiple styles, sizes, and quality options with robust error handling and metadata tracking.

## Features

- 🚀 **Concurrent Generation**: Generate multiple images simultaneously
- 🎨 **Multiple Styles**: Support for 10+ different art styles
- 📐 **Flexible Sizes**: Square, portrait, landscape, wide, and tall formats
- 🔄 **Retry Logic**: Automatic retry with exponential backoff
- 📊 **Metadata Tracking**: Save generation details and results
- 💾 **Local Storage**: Download and save images locally
- ⚙️ **Configuration**: JSON-based configuration support
- 🖥️ **Interactive Mode**: User-friendly interactive interface

## Installation

1. Clone or download the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Interactive Mode (Recommended for beginners)

Simply run the script without arguments:
```bash
python bulk_image_generator.py
```

The tool will prompt you for:
- Flux API key
- Base prompt
- Styles (comma-separated)
- Sizes (comma-separated)
- Prompt variations (optional)

### Command Line Mode

#### Basic Usage
```bash
python bulk_image_generator.py --api-key YOUR_API_KEY --prompt "a beautiful sunset"
```

#### Advanced Usage
```bash
python bulk_image_generator.py \
  --api-key YOUR_API_KEY \
  --prompt "a majestic dragon" \
  --styles realistic anime cyberpunk \
  --sizes square portrait landscape \
  --variations "flying over mountains" "in a cave" "breathing fire" \
  --qualities standard hd \
  --output-dir my_dragons \
  --max-concurrent 3
```

#### Using Configuration File
```bash
python bulk_image_generator.py --config-file config.json --prompt "a magical forest"
```

### List Available Options
```bash
python bulk_image_generator.py --list-options
```

## Configuration

### Available Styles
- `realistic`: Photorealistic images
- `anime`: Anime/manga style
- `cyberpunk`: Cyberpunk art style
- `oil_painting`: Oil painting style
- `watercolor`: Watercolor painting
- `sketch`: Pencil sketch
- `digital_art`: Digital art
- `vintage`: Vintage style
- `futuristic`: Futuristic style
- `minimalist`: Minimalist design

### Available Sizes
- `square`: 1024x1024
- `portrait`: 1024x1408
- `landscape`: 1408x1024
- `wide`: 1792x1024
- `tall`: 1024x1792

### Available Qualities
- `standard`: Standard quality
- `hd`: High definition

### Available Formats
- `png`: PNG format
- `jpeg`: JPEG format
- `webp`: WebP format

## Configuration File

Create a `config.json` file based on the template:

```json
{
  "api_key": "your_flux_api_key_here",
  "base_url": "https://api.flux.ai/v1",
  "max_concurrent": 5,
  "output_dir": "generated_images",
  "save_metadata": true,
  "retry_attempts": 3,
  "retry_delay": 2.0
}
```

## Examples

### Generate Multiple Variations
```bash
python bulk_image_generator.py \
  --api-key YOUR_API_KEY \
  --prompt "a cat" \
  --variations "sleeping" "playing" "hunting" "curious" \
  --styles realistic anime \
  --sizes square portrait
```

### Generate High-Quality Images
```bash
python bulk_image_generator.py \
  --api-key YOUR_API_KEY \
  --prompt "a futuristic cityscape" \
  --styles cyberpunk futuristic \
  --sizes wide landscape \
  --qualities hd \
  --max-concurrent 2
```

### Batch Processing with Configuration
```bash
# Create config.json with your settings
python bulk_image_generator.py \
  --config-file config.json \
  --prompt "a fantasy landscape" \
  --styles oil_painting watercolor \
  --sizes landscape wide
```

## Output Structure

The tool creates the following structure:
```
generated_images/
├── image_001_20241201_143022.png
├── image_002_20241201_143025.png
├── image_003_20241201_143028.png
└── metadata_20241201_143022.json
```

### Metadata File
The metadata file contains:
- Generation timestamp
- Total number of images
- Configuration used
- All requests made
- Results and errors

## Error Handling

The tool includes robust error handling:
- **Rate Limiting**: Automatic retry with exponential backoff
- **Network Errors**: Retry with configurable attempts
- **API Errors**: Detailed error messages
- **Download Failures**: Graceful handling of image download issues

## Performance Tips

1. **Concurrent Requests**: Adjust `--max-concurrent` based on your API limits
2. **Batch Size**: Process images in smaller batches for better reliability
3. **Quality vs Speed**: Use `standard` quality for faster generation
4. **Network**: Ensure stable internet connection for large batches

## Troubleshooting

### Common Issues

1. **API Key Error**: Ensure your Flux API key is valid and has sufficient credits
2. **Rate Limiting**: Reduce `--max-concurrent` value
3. **Network Timeouts**: Increase `retry_delay` in configuration
4. **Disk Space**: Ensure sufficient space in output directory

### Debug Mode
For detailed error information, check the metadata file which contains all request details and error messages.

## API Requirements

- Valid Flux API key
- Sufficient API credits
- Stable internet connection

## License

This tool is provided as-is for educational and personal use.

## Contributing

Feel free to submit issues and enhancement requests!