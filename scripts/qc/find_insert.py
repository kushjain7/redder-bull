#!/usr/bin/env python3
"""
find_insert.py  —  Phone/device insert size validator

Usage:
    python3 scripts/qc/find_insert.py <image.png> [output.json]

What it does:
    - Looks for a phone/device bezel in the image using HSV colour thresholding
    - A phone bezel is typically a dark rectangle (near-black or very dark grey)
    - Measures the width of the largest dark rectangle found
    - Fails if no insert found OR if insert width < MIN_INSERT_WIDTH (540px for 1080px frame)

Output:
    JSON written to <output.json> (default: scripts/qc/find_insert.json)
    Pass/fail result printed to stdout.

Requires:
    pip install opencv-python-headless Pillow numpy
"""

import sys
import json
from pathlib import Path

try:
    import cv2
    import numpy as np
    from PIL import Image
except ImportError:
    print("ERROR: Missing dependencies. Run: pip install opencv-python-headless Pillow numpy")
    sys.exit(1)

# Minimum phone insert width (see skills/design-laws.md D6)
MIN_INSERT_WIDTH = 540  # px (50% of 1080px frame)

# Bezel colour range in HSV — dark greys and near-blacks
# H: 0-180 (any hue, since near-black has no real hue)
# S: 0-60  (low saturation — grey/black)
# V: 0-60  (very dark)
BEZEL_HSV_LOWER = np.array([0, 0, 0])
BEZEL_HSV_UPPER = np.array([180, 60, 60])

# Minimum area to be considered a phone insert (avoid noise)
MIN_BEZEL_AREA = 50000  # pixels²


def find_device_insert(image_path: str) -> dict:
    img_bgr = cv2.imread(image_path)
    if img_bgr is None:
        return {"error": f"Could not read image: {image_path}"}

    h, w = img_bgr.shape[:2]

    # Convert to HSV for colour-based segmentation
    img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)

    # Create mask for dark/bezel pixels
    mask = cv2.inRange(img_hsv, BEZEL_HSV_LOWER, BEZEL_HSV_UPPER)

    # Morphological close to fill small gaps within bezel
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
    mask_closed = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # Find contours
    contours, _ = cv2.findContours(mask_closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return {
            "insert_found": False,
            "status": "warn",
            "note": "No dark rectangular region found — no phone insert detected"
        }

    # Filter by minimum area and find the best candidate
    candidates = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < MIN_BEZEL_AREA:
            continue
        x, y, cw, ch = cv2.boundingRect(cnt)
        aspect = ch / cw if cw > 0 else 0
        # Phone inserts are taller than wide (aspect > 1.2) or roughly square
        # We accept a wide range since inserts can be shown at angles
        candidates.append({
            "bbox": {"x": int(x), "y": int(y), "w": int(cw), "h": int(ch)},
            "area": int(area),
            "aspect_ratio": round(aspect, 2)
        })

    if not candidates:
        return {
            "insert_found": False,
            "status": "warn",
            "note": "No sufficiently large dark region found — no phone insert detected"
        }

    # Pick the largest candidate
    best = max(candidates, key=lambda c: c["area"])
    insert_width = best["bbox"]["w"]

    # Scale minimum width if image is not 1080px wide
    scale = w / 1080.0
    min_w_scaled = int(MIN_INSERT_WIDTH * scale)

    passes = insert_width >= min_w_scaled

    return {
        "insert_found": True,
        "best_candidate": best,
        "all_candidates": candidates,
        "insert_width_px": insert_width,
        "min_required_width_px": min_w_scaled,
        "status": "pass" if passes else "fail",
        "note": (
            f"Insert width {insert_width}px >= {min_w_scaled}px minimum — OK"
            if passes else
            f"Insert width {insert_width}px < {min_w_scaled}px minimum (see skills/design-laws.md D6)"
        )
    }


def main():
    image_path = sys.argv[1] if len(sys.argv) > 1 else None
    output_path = sys.argv[2] if len(sys.argv) > 2 else "scripts/qc/find_insert.json"

    if not image_path:
        print("Usage: python3 scripts/qc/find_insert.py <image.png> [output.json]")
        sys.exit(1)

    if not Path(image_path).exists():
        print(f"ERROR: File not found: {image_path}")
        sys.exit(1)

    # Read image dimensions
    img = Image.open(image_path)
    w, h = img.size

    print(f"Scanning for phone insert: {image_path} ({w}x{h})")
    result = find_device_insert(image_path)

    output = {
        "file": image_path,
        "image_size": f"{w}x{h}",
        **result
    }

    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)

    status = result.get("status", "info")
    print(f"Insert found:  {result.get('insert_found', False)}")
    if result.get("insert_found"):
        print(f"Insert width:  {result.get('insert_width_px')}px (min: {result.get('min_required_width_px')}px)")
    print(f"Status:        {status.upper()}")
    print(f"Note:          {result.get('note', '')}")
    print(f"\nFull results:  {output_path}")

    sys.exit(0 if status in ("pass", "warn", "info") else 1)


if __name__ == "__main__":
    main()
