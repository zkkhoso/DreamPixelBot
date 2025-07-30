# Quick Start Guide

## 🚀 Get Started in 3 Steps

### 1. Setup Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Get Your Flux API Key
- Visit [Flux AI](https://flux.ai) to get your API key
- Or use your existing Flux API key

### 3. Generate Images!

#### Interactive Mode (Easiest)
```bash
python bulk_image_generator.py
```
Just follow the prompts!

#### Command Line Mode
```bash
# Basic usage
python bulk_image_generator.py --api-key YOUR_KEY --prompt "a beautiful sunset"

# Advanced usage
python bulk_image_generator.py \
  --api-key YOUR_KEY \
  --prompt "a majestic dragon" \
  --styles realistic anime \
  --sizes square portrait \
  --variations "flying" "sleeping" "fighting"
```

## 📋 Available Options

### Styles
- `realistic` - Photorealistic images
- `anime` - Anime/manga style
- `cyberpunk` - Cyberpunk art
- `oil_painting` - Oil painting style
- `watercolor` - Watercolor painting
- `sketch` - Pencil sketch
- `digital_art` - Digital art
- `vintage` - Vintage style
- `futuristic` - Futuristic style
- `minimalist` - Minimalist design

### Sizes
- `square` - 1024x1024
- `portrait` - 1024x1408
- `landscape` - 1408x1024
- `wide` - 1792x1024
- `tall` - 1024x1792

### Qualities
- `standard` - Standard quality
- `hd` - High definition

## 🎯 Example Commands

### Generate a Single Image
```bash
python bulk_image_generator.py --api-key YOUR_KEY --prompt "a cute cat"
```

### Generate Multiple Variations
```bash
python bulk_image_generator.py \
  --api-key YOUR_KEY \
  --prompt "a cat" \
  --variations "sleeping" "playing" "hunting" \
  --styles realistic anime
```

### Generate High-Quality Images
```bash
python bulk_image_generator.py \
  --api-key YOUR_KEY \
  --prompt "a futuristic city" \
  --styles cyberpunk \
  --qualities hd \
  --sizes wide
```

### Use Configuration File
```bash
# Edit config_template.json with your API key
python bulk_image_generator.py --config-file config_template.json --prompt "a forest"
```

## 📁 Output

Images are saved to the `generated_images/` directory (or your specified output directory) with:
- Timestamped filenames
- Metadata JSON file with generation details
- Organized structure

## 🔧 Troubleshooting

### Common Issues
1. **"No module named 'aiohttp'"** → Run `pip install -r requirements.txt`
2. **API Key Error** → Check your Flux API key is valid
3. **Rate Limiting** → Reduce `--max-concurrent` value
4. **Permission Denied** → Use virtual environment

### Test Your Setup
```bash
python test_setup.py
```

## 📖 Full Documentation

See `README.md` for complete documentation and advanced features!