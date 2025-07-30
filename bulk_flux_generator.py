import os
import sys
import argparse
import base64
import json
import asyncio
from pathlib import Path

import aiohttp

API_BASE_URL = os.getenv("FLUX_API_BASE", "https://api.deepinfra.com/v1/openai")
DEFAULT_MODEL = os.getenv("FLUX_MODEL", "black-forest-labs/FLUX-pro")


async def generate_image(session: aiohttp.ClientSession, api_key: str, prompt: str, size: str = "1024x1024", model: str = DEFAULT_MODEL, n: int = 1, idx: int = 0, out_dir: Path = Path("outputs")):
    """Send a generation request and save resulting image(s) to disk."""
    url = f"{API_BASE_URL}/images/generations"

    payload = {
        "prompt": prompt,
        "size": size,
        "model": model,
        "n": n,
        "response_format": "b64_json",
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    async with session.post(url, headers=headers, data=json.dumps(payload)) as resp:
        if resp.status != 200:
            text = await resp.text()
            raise RuntimeError(f"API error (status {resp.status}): {text}")

        data = await resp.json()

        for i, item in enumerate(data.get("data", [])):
            b64 = item.get("b64_json")
            if not b64:
                continue
            img_bytes = base64.b64decode(b64)
            out_file = out_dir / f"img_{idx}_{i}.png"
            with open(out_file, "wb") as f:
                f.write(img_bytes)
            print(f"Saved {out_file}")


async def main_async(prompts: list[str], api_key: str, size: str, model: str, n: int, concurrency: int, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)

    connector = aiohttp.TCPConnector(limit_per_host=concurrency)
    async with aiohttp.ClientSession(connector=connector, timeout=aiohttp.ClientTimeout(total=None)) as session:
        tasks = []
        for idx, prompt in enumerate(prompts):
            task = generate_image(session, api_key, prompt, size=size, model=model, n=n, idx=idx, out_dir=out_dir)
            tasks.append(task)
        await asyncio.gather(*tasks)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Bulk image generator using Flux API")
    inp = parser.add_mutually_exclusive_group(required=True)
    inp.add_argument("-p", "--prompts", nargs="*", help="Prompts to generate images for (space separated)")
    inp.add_argument("-f", "--file", type=str, help="Text file containing one prompt per line")

    parser.add_argument("-k", "--api-key", default=os.getenv("FLUX_API_KEY"), help="Flux API key (or set FLUX_API_KEY env var)")
    parser.add_argument("-s", "--size", default="1024x1024", help="Image size, e.g., 1024x1024")
    parser.add_argument("-m", "--model", default=DEFAULT_MODEL, help="Model id to use")
    parser.add_argument("-n", type=int, default=1, help="Number of images per prompt")
    parser.add_argument("-c", "--concurrency", type=int, default=5, help="Number of concurrent API calls")
    parser.add_argument("-o", "--out-dir", type=str, default="outputs", help="Output directory")
    return parser.parse_args()


def main():
    args = parse_args()

    if not args.api_key:
        print("Error: API key is required (use --api-key flag or set FLUX_API_KEY env var)", file=sys.stderr)
        sys.exit(1)

    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            prompts = [line.strip() for line in f if line.strip()]
    else:
        prompts = args.prompts or []

    if not prompts:
        print("Error: No prompts provided", file=sys.stderr)
        sys.exit(1)

    asyncio.run(main_async(prompts, args.api_key, args.size, args.model, args.n, args.concurrency, Path(args.out_dir)))


if __name__ == "__main__":
    main()