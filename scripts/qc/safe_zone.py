#!/usr/bin/env python3
"""
safe_zone.py  —  Instagram Reels safe-zone violation checker

Usage:
    python3 scripts/qc/safe_zone.py <image.png> [output.json]

What it does:
    - Crops the bottom SAFE_B (380px) and top SAFE_T (180px) strips from the frame
    - Runs OCR on those strips
    - Reports any readable text found in the danger zones as a violation

Output:
    JSON written to <output.json> (default: scripts/qc/safe_zone.json)
    Pass/fail result printed to stdout.

Requires:
    pip install pytesseract Pillow
    + tesseract-ocr installed (brew install tesseract)
"""

import sys
import json
from pathlib import Path

try:
    from PIL import Image
    import pytesseract
except ImportError:
    print("ERROR: Missing dependencies. Run: pip install pytesseract Pillow")
    sys.exit(1)

# Safe zone constants (see skills/design-laws.md)
SAFE_T = 180   # px from top
SAFE_B = 380   # px from bottom
SAFE_R = 110   # px from right (checked visually — OCR in right strip too)

MIN_CONFIDENCE = 35   # Tesseract confidence threshold (0-100)


def check_zone(img: Image.Image, zone_name: str, crop_box: tuple) -> dict:
    """OCR a cropped region and return any text found."""
    cropped = img.crop(crop_box)
    try:
        data = pytesseract.image_to_data(cropped, output_type=pytesseract.Output.DICT)
    except Exception as e:
        return {"zone": zone_name, "status": "error", "error": str(e), "text_found": []}

    words = []
    n = len(data["text"])
    for i in range(n):
        word = data["text"][i].strip()
        conf = int(data["conf"][i])
        if conf >= MIN_CONFIDENCE and word and len(word) > 1:
            words.append({
                "word": word,
                "confidence": conf,
                "box_in_crop": {
                    "x": data["left"][i],
                    "y": data["top"][i],
                    "w": data["width"][i],
                    "h": data["height"][i]
                }
            })

    has_violation = len(words) > 0
    return {
        "zone": zone_name,
        "crop_box": crop_box,
        "status": "fail" if has_violation else "pass",
        "violation": has_violation,
        "text_found": words
    }


def analyse(image_path: str, output_path: str) -> dict:
    img = Image.open(image_path)
    width, height = img.size

    # For non-Reels images (not 1080x1920), adjust proportionally or skip
    is_reels = (width == 1080 and height == 1920)
    safe_b = SAFE_B if is_reels else int(height * (SAFE_B / 1920))
    safe_t = SAFE_T if is_reels else int(height * (SAFE_T / 1920))
    safe_r = SAFE_R if is_reels else int(width * (SAFE_R / 1080))

    zones = []

    # Bottom safe zone (most commonly violated)
    bottom_crop = (0, height - safe_b, width - safe_r, height)
    zones.append(check_zone(img, "bottom_safe_zone", bottom_crop))

    # Top safe zone
    top_crop = (0, 0, width - safe_r, safe_t)
    zones.append(check_zone(img, "top_safe_zone", top_crop))

    # Right safe zone (Instagram button column)
    right_crop = (width - safe_r, safe_t, width, height - safe_b)
    zones.append(check_zone(img, "right_safe_zone", right_crop))

    violations = [z for z in zones if z.get("violation")]
    overall = "fail" if violations else "pass"

    output = {
        "file": image_path,
        "image_size": f"{width}x{height}",
        "is_reels_9x16": is_reels,
        "safe_zones_checked": {
            "SAFE_T": safe_t,
            "SAFE_B": safe_b,
            "SAFE_R": safe_r
        },
        "total_violations": len(violations),
        "overall": overall,
        "zones": zones
    }

    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)

    return output


def main():
    image_path = sys.argv[1] if len(sys.argv) > 1 else None
    output_path = sys.argv[2] if len(sys.argv) > 2 else "scripts/qc/safe_zone.json"

    if not image_path:
        print("Usage: python3 scripts/qc/safe_zone.py <image.png> [output.json]")
        sys.exit(1)

    if not Path(image_path).exists():
        print(f"ERROR: File not found: {image_path}")
        sys.exit(1)

    print(f"Checking safe zones: {image_path}")
    result = analyse(image_path, output_path)

    print(f"Image:      {result['image_size']} (Reels: {result['is_reels_9x16']})")
    print(f"Violations: {result['total_violations']}")
    print(f"Overall:    {result['overall'].upper()}")

    if result["total_violations"] > 0:
        print("\nViolations found:")
        for z in result["zones"]:
            if z.get("violation"):
                words = [w["word"] for w in z["text_found"]]
                print(f"  Zone '{z['zone']}': found text → {', '.join(words[:5])}")

    print(f"\nFull results: {output_path}")
    sys.exit(0 if result["overall"] == "pass" else 1)


if __name__ == "__main__":
    main()
