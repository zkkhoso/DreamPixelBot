# Flux Bulk Images Generator - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### 1. Install Dependencies
```bash
pip install aiohttp PyYAML tqdm Pillow
```

### 2. Create Configuration
```bash
python3 flux_bulk_generator.py --create-config
```

### 3. Set Your API Key
Choose one or more providers and set the corresponding environment variable:

```bash
# For DeepInfra (recommended - cost-effective)
export DEEPINFRA_API_KEY="your_deepinfra_api_key"

# For Black Forest Labs (official)
export BFL_API_KEY="your_bfl_api_key"

# For Leonardo AI (feature-rich)
export LEONARDO_API_KEY="your_leonardo_api_key"

# For Replicate (developer-friendly)
export REPLICATE_API_TOKEN="your_replicate_token"
```

### 4. Enable Provider in Configuration
Edit `flux_config.yaml` and set `enabled: true` for your chosen provider:

```yaml
providers:
  deepinfra:
    enabled: true  # Change this to true
    # ... rest of config
```

### 5. Generate Your First Images

#### Single Image
```bash
python3 flux_bulk_generator.py --prompt "A beautiful sunset over mountains"
```

#### Multiple Images
```bash
python3 flux_bulk_generator.py --prompt "Abstract art" --count 5
```

#### From File
```bash
# Create sample prompts first
python3 flux_bulk_generator.py --create-samples

# Generate from file
python3 flux_bulk_generator.py --prompts sample_prompts.txt
```

## 📋 Common Use Cases

### Batch Art Generation
```bash
# Create prompts.txt with one prompt per line
echo "A serene forest landscape
A bustling cyberpunk city
A peaceful mountain lake
A magical wizard tower" > my_prompts.txt

python3 flux_bulk_generator.py --prompts my_prompts.txt
```

### Style Variations
```bash
python3 flux_bulk_generator.py --prompt "Portrait of a cat" --style portrait --size 512x512
```

### Specific Provider
```bash
python3 flux_bulk_generator.py --prompt "Artwork" --provider deepinfra
```

## 📁 File Formats Supported

### Text File (.txt)
```
A magical forest with glowing mushrooms
A futuristic cityscape at night
A peaceful zen garden
```

### JSON File (.json)
```json
[
  {
    "prompt": "A dragon in a medieval castle",
    "size": "1024x1024",
    "style": "dynamic",
    "seed": 42
  },
  {
    "prompt": "A robot in a laboratory",
    "size": "512x512",
    "style": "3d"
  }
]
```

### YAML File (.yaml)
```yaml
- prompt: "A sunset over the ocean"
  size: "1024x1024"
  style: "dynamic"

- prompt: "A portrait of an artist"
  size: "512x512"
  style: "portrait"
  seed: 123
```

## 🎨 Available Styles

- `dynamic` - Vibrant and energetic (default)
- `creative` - Artistic and expressive
- `portrait` - Optimized for faces/people
- `3d` - Three-dimensional rendering
- `anime` - Anime/manga style
- `realistic` - Photorealistic

## 📊 Monitor Progress

The tool provides:
- ✅ Real-time progress bars
- 📄 Detailed logs in `flux_generator.log`
- 📈 JSON results file with metadata
- 🖼️ Auto-organized output in `generated_images/`

## 🛠️ Troubleshooting

### "No providers configured"
- Set your API key: `export DEEPINFRA_API_KEY="your_key"`
- Enable provider in `flux_config.yaml`: `enabled: true`

### "Module not found"
```bash
pip install --break-system-packages aiohttp PyYAML tqdm Pillow
```

### Rate limit issues
- Reduce `max_concurrent` in config
- Increase `retry_delay`

## 💡 Pro Tips

1. **Start small**: Test with 1-3 images first
2. **Use descriptive prompts**: "A serene mountain lake at sunrise with mist"
3. **Batch similar requests**: Group by style or size
4. **Monitor costs**: Check your provider's pricing
5. **Save results**: JSON files contain all metadata

## 🔗 API Provider Sign-ups

- [DeepInfra](https://deepinfra.com/) - $0.04/image, easy setup
- [Black Forest Labs](https://api.bfl.ml/) - Official Flux API
- [Leonardo AI](https://leonardo.ai/) - Feature-rich platform
- [Replicate](https://replicate.com/) - Developer-friendly

## 📚 Next Steps

- Check [README.md](README.md) for complete documentation
- Run [demo_usage.py](demo_usage.py) for examples
- Try [flux_generator_example.ipynb](flux_generator_example.ipynb) for Jupyter usage

## 🆘 Need Help?

1. Check logs: `cat flux_generator.log`
2. Run demo: `python3 demo_usage.py`
3. Verify config: Check `flux_config.yaml`
4. Test single image first before bulk generation

Happy generating! 🎨✨