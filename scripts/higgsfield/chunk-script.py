#!/usr/bin/env python3
"""
chunk-script.py
---------------
Smart chunker for UGC scripts targeting Higgsfield's 8-second hard cap.

Given a plain-text (or markdown fenced-block) script, this tool:
  1. Tokenizes into sentences using both English and Hindi-aware punctuation
  2. Greedily packs sentences into chunks under the 8s budget
  3. Splits oversized single sentences on em-dash / semicolon / comma (in that order)
  4. Never splits mid-number, mid-URL, or mid-bracket
  5. Outputs ugc-chunks.json (with seed_image placeholders ready for run-brief.sh)

Usage:
    python3 scripts/higgsfield/chunk-script.py \
        --script path/to/ugc-script.txt \
        --brief-id 003 \
        --avatar assets/static/avatars/female_25-30_casual_01.jpg \
        --template "kling-video/v2.1/pro/image-to-video" \
        --output path/to/ugc-chunks.json

    # With custom words-per-second (default: 2.4)
    python3 scripts/higgsfield/chunk-script.py \
        --script ugc-script.txt --brief-id 003 --wps 2.2 \
        --avatar assets/static/avatars/... \
        --output ugc-chunks.json

Output JSON format:
    {
      "brief_id": "003",
      "avatar_path": "assets/static/avatars/female_25-30_casual_01.jpg",
      "template": "kling-video/v2.1/pro/image-to-video",
      "aspect": "9:16",
      "wps": 2.4,
      "chunks": [
        {
          "index": 1,
          "text": "...",
          "word_count": 14,
          "est_seconds": 5.83,
          "seed_image": "assets/static/avatars/female_25-30_casual_01.jpg"
        },
        {
          "index": 2,
          "text": "...",
          "word_count": 16,
          "est_seconds": 6.67,
          "seed_image": "creatives/remotion-project/my-ads/public/campaigns/003/ugc/chunk-01-last.jpg"
        }
      ]
    }
"""

import argparse
import json
import re
import sys
from pathlib import Path

MAX_SECONDS = 8.0
TARGET_MAX_SECONDS = 7.5
DEFAULT_WPS = 2.4

# ── Sentence tokenization ────────────────────────────────────────────────────

# Split on sentence-ending punctuation: . ! ? followed by whitespace or end
# Also handles Devanagari danda (।)
SENTENCE_END_RE = re.compile(r'(?<=[.!?।])\s+(?=[^\s])')

# Sub-sentence split points (in priority order)
# Groups: em-dash / en-dash, semicolon, comma
SUB_SPLIT_RE = re.compile(r'\s*[—–;,]\s*')

# Patterns that must NOT be split across
NO_SPLIT_PATTERNS = [
    re.compile(r'[\d,]+(\.\d+)?'),              # numbers like 5,000 or 3.14
    re.compile(r'https?://\S+'),                 # URLs
    re.compile(r'\([^)]*\)'),                    # parenthesised expressions
    re.compile(r'\[[^\]]*\]'),                   # bracketed expressions
    re.compile(r'₹[\d,]+'),                      # Indian rupee amounts
    re.compile(r'\b\d+[kKlL]\b'),               # shorthand like 10k, 5L
]


def estimate_seconds(text: str, wps: float) -> float:
    words = len(text.split())
    return round(words / wps, 2)


def extract_script(raw: str) -> str:
    """Strip markdown fenced code blocks if present, else return raw text."""
    fence_match = re.search(r'```(?:text|script|ugc)?\s*\n(.*?)```', raw, re.DOTALL)
    if fence_match:
        return fence_match.group(1).strip()
    return raw.strip()


def tokenize_sentences(text: str) -> list[str]:
    """Split text into sentences, preserving trailing punctuation."""
    parts = SENTENCE_END_RE.split(text)
    # Clean up and filter empty
    sentences = [p.strip() for p in parts if p.strip()]
    return sentences


def is_safe_split_point(text: str, pos: int) -> bool:
    """Return False if position pos is inside a no-split pattern."""
    for pattern in NO_SPLIT_PATTERNS:
        for m in pattern.finditer(text):
            if m.start() <= pos <= m.end():
                return False
    return True


def split_long_sentence(sentence: str, budget_seconds: float, wps: float) -> list[str]:
    """
    Split a single oversized sentence into chunks that each fit in budget_seconds.
    Splits on em-dash → semicolon → comma, never mid-number/URL/bracket.
    """
    if estimate_seconds(sentence, wps) <= budget_seconds:
        return [sentence]

    # Find all potential split points with priority: em-dash(—/–) > semicolon > comma
    def priority(char: str) -> int:
        return {"—": 0, "–": 0, ";": 1, ",": 2}.get(char, 3)

    candidates: list[tuple[int, int, str]] = []  # (priority, position, char)
    for m in re.finditer(r'[—–;,]', sentence):
        if is_safe_split_point(sentence, m.start()):
            candidates.append((priority(m.group()), m.start(), m.group()))

    if not candidates:
        # No safe split point — return as-is with a warning
        print(
            f"  WARNING: Cannot safely split sentence (no split points found):\n  [{sentence[:80]}...]",
            file=sys.stderr,
        )
        return [sentence]

    # Sort by priority first, then by position (prefer earlier high-priority splits)
    candidates.sort(key=lambda c: (c[0], c[1]))

    # Try splitting at the best candidate that creates two chunks each under budget
    for _, pos, char in candidates:
        left = sentence[:pos].strip()
        right = sentence[pos + len(char):].strip()

        if not left or not right:
            continue

        left_secs = estimate_seconds(left, wps)
        right_secs = estimate_seconds(right, wps)

        if left_secs <= budget_seconds:
            # Recursively handle right side if still too long
            return [left] + split_long_sentence(right, budget_seconds, wps)

    # Could not split sensibly — warn and return whole sentence
    print(
        f"  WARNING: Could not split to fit {budget_seconds}s budget:\n  [{sentence[:80]}...]",
        file=sys.stderr,
    )
    return [sentence]


def pack_chunks(sentences: list[str], max_seconds: float, wps: float) -> list[str]:
    """
    Greedily pack sentences into chunks.
    Each chunk fits within max_seconds. If a single sentence exceeds max_seconds,
    it is split before packing.
    """
    # First expand any sentences that are individually too long
    expanded: list[str] = []
    for s in sentences:
        if estimate_seconds(s, wps) > max_seconds:
            parts = split_long_sentence(s, max_seconds, wps)
            expanded.extend(parts)
        else:
            expanded.append(s)

    chunks: list[str] = []
    current: list[str] = []
    current_secs = 0.0

    for sentence in expanded:
        s_secs = estimate_seconds(sentence, wps)

        if current and current_secs + s_secs > max_seconds:
            # Flush current chunk
            chunks.append(" ".join(current))
            current = [sentence]
            current_secs = s_secs
        else:
            current.append(sentence)
            current_secs += s_secs

    if current:
        chunks.append(" ".join(current))

    return chunks


def build_output(
    brief_id: str,
    avatar_path: str,
    template: str,
    chunks: list[str],
    wps: float,
) -> dict:
    campaign_dir = f"creatives/remotion-project/my-ads/public/campaigns/{brief_id}/ugc"
    result: dict = {
        "brief_id": brief_id,
        "avatar_path": avatar_path,
        "template": template,
        "aspect": "9:16",
        "wps": wps,
        "chunks": [],
    }

    for i, text in enumerate(chunks, start=1):
        word_count = len(text.split())
        est_seconds = estimate_seconds(text, wps)

        if i == 1:
            seed_image = avatar_path
        else:
            seed_image = f"{campaign_dir}/chunk-{i - 1:02d}-last.jpg"

        result["chunks"].append(
            {
                "index": i,
                "text": text,
                "word_count": word_count,
                "est_seconds": est_seconds,
                "seed_image": seed_image,
            }
        )

    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Smart-chunk a UGC script into Higgsfield-compatible 8s blocks."
    )
    parser.add_argument("--script", required=True, help="Path to the UGC script file")
    parser.add_argument("--brief-id", required=True, help="Brief ID (e.g. 003)")
    parser.add_argument(
        "--avatar",
        required=True,
        help="Relative path to the avatar image (e.g. assets/static/avatars/female_25-30_casual_01.jpg)",
    )
    parser.add_argument(
        "--template",
        default="kling-video/v2.1/pro/image-to-video",
        help="Higgsfield model ID to use (default: kling-video/v2.1/pro/image-to-video)",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output path for ugc-chunks.json",
    )
    parser.add_argument(
        "--wps",
        type=float,
        default=DEFAULT_WPS,
        help=f"Words per second speaking rate (default: {DEFAULT_WPS})",
    )
    parser.add_argument(
        "--max-seconds",
        type=float,
        default=TARGET_MAX_SECONDS,
        help=f"Max seconds per chunk (default: {TARGET_MAX_SECONDS}; hard cap is {MAX_SECONDS})",
    )
    args = parser.parse_args()

    if args.max_seconds > MAX_SECONDS:
        print(
            f"ERROR: --max-seconds {args.max_seconds} exceeds Higgsfield's hard cap of {MAX_SECONDS}s.",
            file=sys.stderr,
        )
        sys.exit(1)

    script_path = Path(args.script)
    if not script_path.exists():
        print(f"ERROR: Script file not found: {script_path}", file=sys.stderr)
        sys.exit(1)

    raw = script_path.read_text(encoding="utf-8")
    script = extract_script(raw)

    if not script:
        print("ERROR: Script is empty after extraction.", file=sys.stderr)
        sys.exit(1)

    sentences = tokenize_sentences(script)

    if not sentences:
        print("ERROR: Could not tokenize any sentences from the script.", file=sys.stderr)
        sys.exit(1)

    print(f"Script: {len(sentences)} sentence(s), "
          f"~{estimate_seconds(script, args.wps):.1f}s total at {args.wps} wps")

    chunks = pack_chunks(sentences, args.max_seconds, args.wps)

    print(f"Chunked into {len(chunks)} chunk(s):")
    for i, chunk in enumerate(chunks, start=1):
        secs = estimate_seconds(chunk, args.wps)
        flag = " ⚠ OVER BUDGET" if secs > MAX_SECONDS else ""
        print(f"  Chunk {i}: {len(chunk.split()):>3} words, ~{secs:.2f}s{flag}")

    output_data = build_output(
        brief_id=args.brief_id,
        avatar_path=args.avatar,
        template=args.template,
        chunks=chunks,
        wps=args.wps,
    )

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output_data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nWrote {len(chunks)} chunks → {output_path}")

    # Check for over-budget chunks and warn
    over_budget = [
        c for c in output_data["chunks"] if c["est_seconds"] > MAX_SECONDS
    ]
    if over_budget:
        print(f"\nWARNING: {len(over_budget)} chunk(s) exceed {MAX_SECONDS}s — review manually before generation.")
        sys.exit(2)


if __name__ == "__main__":
    main()
