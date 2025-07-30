# Flux Bulk Images Generator

A powerful command-line tool for generating multiple images in bulk using various Flux API providers. This tool supports multiple providers including Black Forest Labs, DeepInfra, Leonardo AI, and Replicate, allowing you to generate hundreds of images efficiently with proper rate limiting, error handling, and progress tracking.

## Features

- 🚀 **Multiple Provider Support**: Works with Black Forest Labs, DeepInfra, Leonardo AI, and Replicate APIs
- ⚡ **Bulk Generation**: Generate hundreds of images in parallel with configurable concurrency
- 📊 **Progress Tracking**: Real-time progress bars and detailed logging
- 🔄 **Error Handling**: Automatic retries with exponential backoff
- 📁 **Flexible Input**: Support for JSON, YAML, and TXT prompt files
- 🎨 **Style Controls**: Various image styles and quality settings
- 💾 **Auto-Save**: Automatic image saving with organized file naming
- 📈 **Results Tracking**: JSON reports of all generation attempts

## Installation

1. Clone or download the repository:
```bash
git clone <repository-url>
cd flux-bulk-generator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install aiohttp PyYAML tqdm Pillow
```

## Quick Start

1. **Create configuration file**:
```bash
python3 flux_bulk_generator.py --create-config
```

2. **Create sample prompts**:
```bash
python3 flux_bulk_generator.py --create-samples
```

3. **Edit `flux_config.yaml`** with your API keys and enable desired providers

4. **Generate images**:
```bash
# Generate from prompt file
python3 flux_bulk_generator.py --prompts sample_prompts.txt

# Generate single prompt
python3 flux_bulk_generator.py --prompt "A futuristic cityscape at sunset"

# Generate multiple copies
python3 flux_bulk_generator.py --prompt "Abstract art" --count 5
```

## Configuration

The tool uses a YAML configuration file (`flux_config.yaml`) to manage API providers and settings.

### Sample Configuration

```yaml
providers:
  black_forest_labs:
    enabled: true
    api_key_env: "BFL_API_KEY"
    base_url: "https://api.bfl.ml"
    model_id: "flux-pro-1.1"
    max_concurrent: 3
    retry_attempts: 3
    retry_delay: 1.0

  deepinfra:
    enabled: true
    api_key_env: "DEEPINFRA_API_KEY"
    base_url: "https://api.deepinfra.com"
    model_id: "black-forest-labs/FLUX-1.1-pro"
    max_concurrent: 5
    retry_attempts: 3
    retry_delay: 1.0

  leonardo:
    enabled: false
    api_key_env: "LEONARDO_API_KEY"
    base_url: "https://cloud.leonardo.ai"
    model_id: "b2614463-296c-462a-9586-aafdb8f00e36"
    max_concurrent: 3
    retry_attempts: 3
    retry_delay: 2.0

  replicate:
    enabled: false
    api_key_env: "REPLICATE_API_TOKEN"
    base_url: "https://api.replicate.com"
    model_id: "black-forest-labs/flux-pro"
    max_concurrent: 3
    retry_attempts: 3
    retry_delay: 1.0

default_settings:
  size: "1024x1024"
  style: "dynamic"
  quality: "standard"
  output_format: "png"
```

### Environment Variables

Set your API keys as environment variables:

```bash
export BFL_API_KEY="your_black_forest_labs_api_key"
export DEEPINFRA_API_KEY="your_deepinfra_api_key"
export LEONARDO_API_KEY="your_leonardo_api_key"
export REPLICATE_API_TOKEN="your_replicate_api_token"
```

## Usage Examples

### Command Line Options

```bash
python3 flux_bulk_generator.py [OPTIONS]

Options:
  --config PATH           Configuration file path (default: flux_config.yaml)
  --prompts PATH          Prompts file path (JSON, YAML, or TXT)
  --prompt TEXT           Single prompt to generate
  --provider NAME         Specific provider to use
  --size SIZE             Image size (default: 1024x1024)
  --style STYLE           Image style (default: dynamic)
  --count NUMBER          Number of images for single prompt (default: 1)
  --output-dir PATH       Output directory for generated images
  --create-config         Create sample configuration file
  --create-samples        Create sample prompt files
```

### Prompt File Formats

#### JSON Format (`prompts.json`)
```json
[
  {
    "prompt": "A futuristic cityscape at sunset with flying cars",
    "size": "1024x1024",
    "style": "dynamic",
    "seed": 12345
  },
  {
    "prompt": "A serene mountain landscape",
    "size": "1024x1024",
    "style": "creative"
  }
]
```

#### YAML Format (`prompts.yaml`)
```yaml
- prompt: "A magical forest with glowing mushrooms"
  size: "1024x1024"
  style: "dynamic"

- prompt: "A steampunk robot in a Victorian laboratory"
  size: "1024x1024"
  style: "creative"
  seed: 54321
```

#### Text Format (`prompts.txt`)
```
A magical forest with glowing mushrooms and fireflies
A steampunk robot in a Victorian laboratory
An underwater city with bioluminescent architecture
A space station orbiting a colorful nebula
```

### Advanced Usage

#### Generate with specific provider
```bash
python3 flux_bulk_generator.py --prompts prompts.json --provider deepinfra
```

#### Custom output directory
```bash
python3 flux_bulk_generator.py --prompt "Abstract art" --output-dir ./my_images
```

#### Different image sizes and styles
```bash
python3 flux_bulk_generator.py --prompt "Portrait of a cat" --size 512x512 --style portrait
```

#### Multiple copies with variations
```bash
python3 flux_bulk_generator.py --prompt "Landscape painting" --count 10
```

## API Provider Details

### Black Forest Labs
- **Official Flux API**
- Models: flux-pro-1.1, flux-pro
- High quality, latest models
- Requires BFL API key

### DeepInfra
- **Cost-effective option**
- Models: black-forest-labs/FLUX-1.1-pro, black-forest-labs/FLUX-pro
- Good performance, competitive pricing
- Requires DeepInfra API key

### Leonardo AI
- **Feature-rich platform**
- Advanced style controls and presets
- Built-in enhancement features
- Requires Leonardo API key

### Replicate
- **Developer-friendly**
- Easy integration, good documentation
- Per-prediction pricing
- Requires Replicate API token

## Image Styles

Available styles (provider-dependent):

- `dynamic` - Vibrant and energetic
- `creative` - Artistic and expressive
- `portrait` - Optimized for faces/people
- `3d` - Three-dimensional rendering
- `anime` - Anime/manga style
- `realistic` - Photorealistic
- `artistic` - Painterly effects

## Output Organization

Generated images are saved in the `generated_images/` directory (or custom path) with:

- **Organized naming**: `YYYYMMDD_HHMMSS_provider.png`
- **Results JSON**: Detailed generation results and metadata
- **Log files**: Complete operation logs in `flux_generator.log`

## Error Handling

The tool includes robust error handling:

- **Automatic retries** with exponential backoff
- **Rate limiting** with configurable concurrency
- **Provider failover** (when multiple providers enabled)
- **Detailed error logging** for troubleshooting
- **Graceful degradation** - continues with successful generations

## Performance Tips

1. **Optimize concurrency**: Adjust `max_concurrent` based on your API limits
2. **Use appropriate retry settings**: Balance speed vs reliability
3. **Choose the right provider**: Consider cost, speed, and quality needs
4. **Batch your requests**: Use prompt files for bulk operations
5. **Monitor rate limits**: Check provider documentation for limits

## Troubleshooting

### Common Issues

1. **Module not found errors**:
   ```bash
   pip install --break-system-packages aiohttp PyYAML tqdm Pillow
   ```

2. **API key not found**:
   - Check environment variables are set
   - Verify configuration file has correct `api_key_env` values

3. **Rate limit exceeded**:
   - Reduce `max_concurrent` in configuration
   - Increase `retry_delay`

4. **Generation failures**:
   - Check API key validity
   - Verify provider endpoints are accessible
   - Review logs in `flux_generator.log`

### Debug Mode

Enable detailed logging by editing the log level in the script:
```python
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with multiple providers
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Black Forest Labs for the amazing Flux models
- All API providers for making these models accessible
- The Python async community for excellent libraries

## Support

For issues and questions:

1. Check the troubleshooting section
2. Review the logs in `flux_generator.log`
3. Open an issue with detailed error information
4. Include your configuration (without API keys)