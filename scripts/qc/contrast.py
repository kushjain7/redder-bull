#!/usr/bin/env python3
"""
contrast.py  —  WCAG AA contrast checker for ad creatives

Usage:
    python3 scripts/qc/contrast.py <image.png> [output.json]

What it does:
    - Runs OCR via pytesseract to find text bounding boxes
    - For each text region, samples the average text colour and background colour
    - Computes WCAG 2.1 relative luminance contrast ratio
    - Flags any text region with contrast < 4.5:1 (WCAG AA fail)

Output:
    JSON written to <output.json> (default: scripts/qc/contrast.json)
    Pass/fail result printed to stdout.

Requires:
    pip install pytesseract Pillow
    + tesseract-ocr installed on system (brew install tesseract)
"""

import sys
import json
import math
from pathlib import Path

try:
    from PIL import Image, ImageFilter
    import pytesseract
except ImportError:
    print("ERROR: Missing dependencies. Run: pip install pytesseract Pillow")
    print("       Also: brew install tesseract")
    sys.exit(1)


def srgb_to_linear(channel: float) -> float:
    """Convert sRGB 0-1 to linear light (IEC 61966-2-1)."""
    if channel <= 0.04045:
        return channel / 12.92
    return ((channel + 0.055) / 1.055) ** 2.4


def relative_luminance(r: int, g: int, b: int) -> float:
    """WCAG 2.1 relative luminance for an sRGB colour (0-255 each channel)."""
    lr = srgb_to_linear(r / 255.0)
    lg = srgb_to_linear(g / 255.0)
    lb = srgb_to_linear(b / 255.0)
    return 0.2126 * lr + 0.7152 * lg + 0.0722 * lb


def contrast_ratio(lum1: float, lum2: float) -> float:
    lighter = max(lum1, lum2)
    darker = min(lum1, lum2)
    return (lighter + 0.05) / (darker + 0.05)


def sample_region_colour(img: Image.Image, box: tuple, is_text: bool) -> tuple:
    """
    Sample average colour in a region.
    For text: sample the darkest 20% of pixels (text colour).
    For background: sample from a slightly enlarged region, excluding text pixels.
    """
    x, y, w, h = box
    region = img.crop((x, y, x + w, y + h)).convert("RGB")
    pixels = list(region.getdata())
    if not pixels:
        return (128, 128, 128)

    # Sort by luminance
    lums = [(relative_luminance(px[0], px[1], px[2]), px) for px in pixels]
    lums.sort(key=lambda x: x[0])

    if is_text:
        # Text is usually the darker pixels
        sample = [px for _, px in lums[:max(1, len(lums)//5)]]
    else:
        # Background is usually the lighter pixels
        sample = [px for _, px in lums[max(0, len(lums)*4//5):]]

    avg_r = int(sum(p[0] for p in sample) / len(sample))
    avg_g = int(sum(p[1] for p in sample) / len(sample))
    avg_b = int(sum(p[2] for p in sample) / len(sample))
    return (avg_r, avg_g, avg_b)


def analyse(image_path: str, output_path: str) -> dict:
    img = Image.open(image_path)
    width, height = img.size

    # OCR: get word-level bounding boxes
    try:
        data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
    except Exception as e:
        return {
            "error": f"OCR failed: {e}",
            "status": "error",
            "file": image_path
        }

    results = []
    n = len(data["text"])

    for i in range(n):
        word = data["text"][i].strip()
        conf = int(data["conf"][i])
        if conf < 30 or not word:
            continue

        x, y, w, h = data["left"][i], data["top"][i], data["width"][i], data["height"][i]
        if w < 5 or h < 5:
            continue

        # Sample text colour (dark pixels in box)
        text_colour = sample_region_colour(img, (x, y, w, h), is_text=True)

        # Sample background: slightly expand the box
        pad = max(4, h // 4)
        bg_x = max(0, x - pad)
        bg_y = max(0, y - pad)
        bg_w = min(width - bg_x, w + 2 * pad)
        bg_h = min(height - bg_y, h + 2 * pad)
        bg_colour = sample_region_colour(img, (bg_x, bg_y, bg_w, bg_h), is_text=False)

        text_lum = relative_luminance(*text_colour)
        bg_lum = relative_luminance(*bg_colour)
        ratio = contrast_ratio(text_lum, bg_lum)

        wcag_aa = ratio >= 4.5
        wcag_aaa = ratio >= 7.0

        results.append({
            "word": word,
            "box": {"x": x, "y": y, "w": w, "h": h},
            "text_colour_rgb": text_colour,
            "bg_colour_rgb": bg_colour,
            "contrast_ratio": round(ratio, 2),
            "wcag_aa": wcag_aa,
            "wcag_aaa": wcag_aaa,
            "status": "pass" if wcag_aa else "fail"
        })

    fails = [r for r in results if not r["wcag_aa"]]
    overall = "pass" if not fails else "fail"

    output = {
        "file": image_path,
        "image_size": f"{width}x{height}",
        "total_words_checked": len(results),
        "wcag_aa_fails": len(fails),
        "overall": overall,
        "results": results
    }

    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)

    return output


def main():
    image_path = sys.argv[1] if len(sys.argv) > 1 else None
    output_path = sys.argv[2] if len(sys.argv) > 2 else "scripts/qc/contrast.json"

    if not image_path:
        print("Usage: python3 scripts/qc/contrast.py <image.png> [output.json]")
        sys.exit(1)

    if not Path(image_path).exists():
        print(f"ERROR: File not found: {image_path}")
        sys.exit(1)

    print(f"Checking contrast: {image_path}")
    result = analyse(image_path, output_path)

    if "error" in result:
        print(f"ERROR: {result['error']}")
        sys.exit(1)

    print(f"Words checked:   {result['total_words_checked']}")
    print(f"WCAG AA fails:   {result['wcag_aa_fails']}")
    print(f"Overall:         {result['overall'].upper()}")

    if result["wcag_aa_fails"] > 0:
        print("\nFailing elements:")
        for r in result["results"]:
            if not r["wcag_aa"]:
                print(f"  '{r['word']}' at ({r['box']['x']},{r['box']['y']}) — ratio {r['contrast_ratio']}:1")

    print(f"\nFull results: {output_path}")

    sys.exit(0 if result["overall"] == "pass" else 1)


if __name__ == "__main__":
    main()
