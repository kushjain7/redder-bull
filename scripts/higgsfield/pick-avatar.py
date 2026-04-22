#!/usr/bin/env python3
"""
pick-avatar.py
--------------
Find the best-matching avatar from assets/static/avatars/_metadata.json
based on brief tags (gender, age-band, vibe).

Usage:
    python3 scripts/higgsfield/pick-avatar.py \
        --gender female \
        --age-band "25-30" \
        --vibe confessional

Returns:
    Prints the relative file path to stdout (e.g. assets/static/avatars/female_25-30_casual_01.jpg)
    Exits 0 on success, 1 if no suitable avatar is found.

Matching strategy (highest to lowest priority):
    1. Exact match on all three fields
    2. Match on gender + age-band (any vibe)
    3. Match on gender + vibe (any age-band)
    4. Match on gender alone
    5. Any available avatar

"vibe" matching treats adjacent vibes as equivalent:
    confessional ↔ relatable ↔ casual
    demo ↔ tech-savvy ↔ professional
    day-in-the-life ↔ aspirational ↔ casual
    reaction ↔ energetic ↔ relatable
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parents[2]
METADATA_PATH = REPO_ROOT / "assets" / "static" / "avatars" / "_metadata.json"

VIBE_EQUIVALENTS: dict[str, list[str]] = {
    "confessional":    ["confessional", "relatable", "casual"],
    "relatable":       ["relatable", "casual", "confessional"],
    "casual":          ["casual", "relatable", "confessional"],
    "demo":            ["demo", "tech-savvy", "professional"],
    "tech-savvy":      ["tech-savvy", "professional", "demo"],
    "professional":    ["professional", "tech-savvy", "demo"],
    "day-in-the-life": ["day-in-the-life", "aspirational", "casual"],
    "aspirational":    ["aspirational", "casual", "day-in-the-life"],
    "reaction":        ["reaction", "energetic", "relatable"],
    "energetic":       ["energetic", "reaction", "relatable"],
}


def load_metadata() -> list[dict]:
    if not METADATA_PATH.exists():
        print(f"ERROR: Metadata file not found: {METADATA_PATH}", file=sys.stderr)
        sys.exit(1)

    data = json.loads(METADATA_PATH.read_text())
    avatars = data.get("avatars", [])

    if not avatars:
        print(
            "ERROR: No avatars registered in _metadata.json. "
            "Add avatar images and metadata entries first.\n"
            "See assets/static/avatars/README.md for instructions.",
            file=sys.stderr,
        )
        sys.exit(1)

    return avatars


def score_avatar(avatar: dict, gender: str, age_band: str, vibe: str) -> int:
    """
    Returns a match score (higher is better).
    Exact match on all three = 7.
    """
    gender_match = avatar.get("gender", "").lower() == gender.lower()
    age_match = avatar.get("age_band", "") == age_band
    avatar_vibe = avatar.get("vibe", "").lower()

    vibe_equivalents = VIBE_EQUIVALENTS.get(vibe.lower(), [vibe.lower()])
    vibe_exact = avatar_vibe == vibe.lower()
    vibe_near = avatar_vibe in vibe_equivalents

    score = 0
    if gender_match:
        score += 4
    if age_match:
        score += 2
    if vibe_exact:
        score += 1
    elif vibe_near:
        score += 0

    # Also check recommended_for field
    rec_for = [r.lower() for r in avatar.get("recommended_for", [])]
    if vibe.lower() in rec_for:
        score += 1

    return score


def pick_best(avatars: list[dict], gender: str, age_band: str, vibe: str) -> Optional[dict]:
    scored = [(score_avatar(a, gender, age_band, vibe), a) for a in avatars]
    scored.sort(key=lambda x: -x[0])

    if not scored:
        return None

    best_score, best_avatar = scored[0]
    if best_score == 0:
        return None  # Not even a gender match

    return best_avatar


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Find the best-matching avatar image for a brief."
    )
    parser.add_argument("--gender", required=True, help="female | male | neutral")
    parser.add_argument(
        "--age-band", required=True, help="18-24 | 25-30 | 30-35 | 35-45"
    )
    parser.add_argument(
        "--vibe",
        required=True,
        help="casual | confessional | aspirational | professional | energetic | relatable | tech-savvy | demo | day-in-the-life | reaction",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="Print all available avatars and exit.",
    )
    args = parser.parse_args()

    avatars = load_metadata()

    if args.list:
        print("Available avatars:")
        for av in avatars:
            print(f"  {av['filename']:45s}  gender={av['gender']:<8} age={av['age_band']:<7} vibe={av['vibe']}")
        return

    best = pick_best(avatars, args.gender, args.age_band, args.vibe)

    if best is None:
        print(
            f"ERROR: No suitable avatar found for gender={args.gender}, "
            f"age_band={args.age_band}, vibe={args.vibe}. "
            "Add a matching avatar to assets/static/avatars/ and register it in _metadata.json.",
            file=sys.stderr,
        )
        sys.exit(1)

    avatar_path = REPO_ROOT / "assets" / "static" / "avatars" / best["filename"]
    if not avatar_path.exists():
        print(
            f"ERROR: Avatar file not found on disk: {avatar_path}\n"
            "Image file is missing — add it to assets/static/avatars/.",
            file=sys.stderr,
        )
        sys.exit(1)

    rel_path = avatar_path.relative_to(REPO_ROOT)
    print(str(rel_path))


if __name__ == "__main__":
    main()
