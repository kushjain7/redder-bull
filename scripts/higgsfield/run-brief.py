#!/usr/bin/env python3
"""
run-brief.py
------------
Automated UGC chunk generation via Higgsfield API.

Reads a ugc-chunks.json manifest, generates each chunk via the Higgsfield
Python SDK, downloads the resulting MP4s, extracts last-frames for chaining,
and writes a ugc-chunks-report.json.

Usage:
    python3 scripts/higgsfield/run-brief.py \
        --chunks path/to/ugc-chunks.json \
        [--dry-run]   # prints plan without calling API

Environment (from scripts/higgsfield/higgsfield.local.env):
    HF_API_KEY     — Higgsfield API key
    HF_API_SECRET  — Higgsfield API secret

Folder created automatically:
    creatives/remotion-project/my-ads/public/campaigns/{brief_id}/ugc/
"""

from __future__ import annotations

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = Path(__file__).parent / "higgsfield.local.env"

# Retry settings
MAX_RETRIES = 2
RETRY_DELAY_SECONDS = 15


# ── Credential loading ────────────────────────────────────────────────────────

def load_env() -> None:
    """Load API credentials from higgsfield.local.env into os.environ."""
    if not ENV_PATH.exists():
        print(
            f"ERROR: Credentials file not found: {ENV_PATH}\n"
            "Run bash scripts/higgsfield/setup-playwright.sh first.",
            file=sys.stderr,
        )
        sys.exit(1)

    for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, _, v = line.partition("=")
            os.environ.setdefault(k.strip(), v.strip())

    key = os.environ.get("HF_API_KEY", "")
    secret = os.environ.get("HF_API_SECRET", "")

    if not key or key == "your_api_key_here":
        print(
            "ERROR: HF_API_KEY is not set. Edit scripts/higgsfield/higgsfield.local.env.",
            file=sys.stderr,
        )
        sys.exit(1)

    if not secret or secret == "your_api_secret_here":
        print(
            "ERROR: HF_API_SECRET is not set. Edit scripts/higgsfield/higgsfield.local.env.",
            file=sys.stderr,
        )
        sys.exit(1)


# ── SDK import ────────────────────────────────────────────────────────────────

def import_sdk():
    try:
        import higgsfield_client
        return higgsfield_client
    except ImportError:
        print(
            "ERROR: higgsfield-client not installed.\n"
            "Run: pip3 install higgsfield-client requests",
            file=sys.stderr,
        )
        sys.exit(1)


# ── File helpers ─────────────────────────────────────────────────────────────

def download_file(url: str, dest: Path) -> None:
    import requests

    dest.parent.mkdir(parents=True, exist_ok=True)
    with requests.get(url, stream=True, timeout=120) as r:
        r.raise_for_status()
        with open(dest, "wb") as f:
            for block in r.iter_content(chunk_size=8192):
                f.write(block)


def extract_last_frame(video_path: Path, out_path: Path) -> bool:
    """Extract the last frame of a video using ffmpeg. Returns True on success."""
    result = subprocess.run(
        [
            "ffmpeg", "-y",
            "-sseof", "-0.1",
            "-i", str(video_path),
            "-frames:v", "1",
            "-update", "1",
            str(out_path),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"  WARNING: ffmpeg last-frame extraction failed:\n{result.stderr}", file=sys.stderr)
        return False
    return True


def get_video_duration(video_path: Path) -> Optional[float]:
    """Return video duration in seconds via ffprobe. Returns None on failure."""
    result = subprocess.run(
        [
            "ffprobe", "-v", "quiet",
            "-show_entries", "format=duration",
            "-of", "csv=p=0",
            str(video_path),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    try:
        return float(result.stdout.strip())
    except ValueError:
        return None


# ── Generation ────────────────────────────────────────────────────────────────

def generate_chunk(
    hf,
    chunk: dict,
    template: str,
    dry_run: bool,
) -> str | None:
    """
    Submit generation for a single chunk.
    Returns the video URL on success, None on failure.
    """
    if dry_run:
        print(f"  [DRY RUN] Would generate: {chunk['text'][:60]}...")
        return "DRY_RUN_URL"

    seed_image = chunk["seed_image"]
    text = chunk["text"]

    # Upload seed image (it may be a local path or already a URL)
    if seed_image.startswith("http"):
        image_url = seed_image
    else:
        seed_path = REPO_ROOT / seed_image
        if not seed_path.exists():
            print(f"  ERROR: Seed image not found: {seed_path}", file=sys.stderr)
            return None
        print(f"  Uploading seed image: {seed_path.name} ...")
        image_url = hf.upload_file(str(seed_path))

    for attempt in range(1, MAX_RETRIES + 2):
        try:
            print(f"  Submitting to {template} (attempt {attempt})...")
            result = hf.subscribe(
                template,
                arguments={
                    "image_url": image_url,
                    "prompt": text,
                    "duration": 5,
                    "aspect_ratio": "9:16",
                },
            )
            video_url = result.get("video", {}).get("url")
            if video_url:
                return video_url
            print(f"  No video URL in response: {result}", file=sys.stderr)
            return None

        except Exception as exc:
            msg = str(exc)
            if "nsfw" in msg.lower():
                print(f"  NSFW rejection — chunk skipped.", file=sys.stderr)
                return None
            if "credit" in msg.lower() or "402" in msg:
                print(f"  Credit exhaustion — stopping.", file=sys.stderr)
                sys.exit(1)
            if attempt <= MAX_RETRIES:
                print(f"  Error (attempt {attempt}): {msg} — retrying in {RETRY_DELAY_SECONDS}s...")
                time.sleep(RETRY_DELAY_SECONDS)
            else:
                print(f"  ERROR: {msg}", file=sys.stderr)
                return None

    return None


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate all UGC chunks from a ugc-chunks.json manifest."
    )
    parser.add_argument(
        "--chunks",
        required=True,
        help="Path to ugc-chunks.json produced by chunk-script.py",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the plan without calling the API",
    )
    parser.add_argument(
        "--start-from",
        type=int,
        default=1,
        help="Resume from chunk N (1-indexed). Skips earlier chunks.",
    )
    args = parser.parse_args()

    chunks_path = Path(args.chunks)
    if not chunks_path.exists():
        print(f"ERROR: Chunks manifest not found: {chunks_path}", file=sys.stderr)
        sys.exit(1)

    manifest = json.loads(chunks_path.read_text(encoding="utf-8"))
    brief_id = manifest["brief_id"]
    template = manifest["template"]
    chunks = manifest["chunks"]

    out_dir = REPO_ROOT / "creatives" / "remotion-project" / "my-ads" / "public" / "campaigns" / brief_id / "ugc"
    report_path = chunks_path.parent / "ugc-chunks-report.json"

    print(f"=== Higgsfield UGC Generation — Brief {brief_id} ===")
    print(f"Template  : {template}")
    print(f"Chunks    : {len(chunks)}")
    print(f"Output dir: {out_dir.relative_to(REPO_ROOT)}")
    print()

    if not args.dry_run:
        load_env()
        hf = import_sdk()
        out_dir.mkdir(parents=True, exist_ok=True)
    else:
        hf = None

    report: list[dict] = []
    current_seed_url: str | None = None

    for chunk in chunks:
        idx = chunk["index"]

        if idx < args.start_from:
            print(f"Chunk {idx:02d}: skipping (--start-from={args.start_from})")
            continue

        print(f"Chunk {idx:02d}: [{chunk['text'][:60]}...]")
        print(f"  Estimated: {chunk['est_seconds']:.2f}s, seed: {chunk['seed_image'].split('/')[-1]}")

        chunk_mp4 = out_dir / f"chunk-{idx:02d}.mp4"
        chunk_last = out_dir / f"chunk-{idx:02d}-last.jpg"

        # If seed for this chunk is the last-frame of previous, use what we extracted
        if current_seed_url and not chunk["seed_image"].startswith("assets/static"):
            chunk = dict(chunk)
            chunk["seed_image"] = current_seed_url  # already-uploaded URL

        video_url = generate_chunk(hf, chunk, template, args.dry_run)

        entry: dict = {
            "index": idx,
            "text_preview": chunk["text"][:80],
            "est_seconds": chunk["est_seconds"],
            "status": "pending",
            "video_url": None,
            "local_path": None,
            "actual_duration": None,
            "last_frame": None,
            "generated_at": None,
        }

        if not video_url:
            entry["status"] = "failed"
            report.append(entry)
            print(f"  ✗ Generation failed for chunk {idx}")
            continue

        if args.dry_run:
            entry["status"] = "dry_run"
            report.append(entry)
            print(f"  ✓ Dry run OK")
            continue

        entry["video_url"] = video_url
        entry["generated_at"] = datetime.now(timezone.utc).isoformat()

        print(f"  Downloading → {chunk_mp4.name} ...")
        try:
            download_file(video_url, chunk_mp4)
        except Exception as exc:
            print(f"  ✗ Download failed: {exc}", file=sys.stderr)
            entry["status"] = "download_failed"
            report.append(entry)
            continue

        actual_duration = get_video_duration(chunk_mp4)
        entry["local_path"] = str(chunk_mp4.relative_to(REPO_ROOT))
        entry["actual_duration"] = actual_duration

        # Sanity check duration
        if actual_duration is not None and (actual_duration < 1.0 or actual_duration > 9.0):
            print(f"  ⚠ Unusual duration: {actual_duration:.2f}s")

        # Extract last frame for next chunk's seed
        print(f"  Extracting last frame → {chunk_last.name} ...")
        if extract_last_frame(chunk_mp4, chunk_last):
            entry["last_frame"] = str(chunk_last.relative_to(REPO_ROOT))
            # Upload last frame so it's ready as URL for next chunk
            print(f"  Uploading last frame for chaining...")
            try:
                current_seed_url = hf.upload_file(str(chunk_last))
            except Exception as exc:
                print(f"  WARNING: Could not upload last frame: {exc}", file=sys.stderr)
                current_seed_url = None
        else:
            current_seed_url = None

        entry["status"] = "completed"
        print(f"  ✓ Chunk {idx:02d} done ({actual_duration:.2f}s actual)")
        report.append(entry)

    # ── Write report ──────────────────────────────────────────────────────────
    report_data = {
        "brief_id": brief_id,
        "template": template,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_chunks": len(chunks),
        "completed": sum(1 for r in report if r["status"] == "completed"),
        "failed": sum(1 for r in report if r["status"] in ("failed", "download_failed")),
        "chunks": report,
    }

    report_path.write_text(
        json.dumps(report_data, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"\nReport written → {report_path}")

    failed_count = report_data["failed"]
    if failed_count > 0:
        print(f"\n✗ {failed_count} chunk(s) failed. Review ugc-chunks-report.json and re-run with --start-from.")
        sys.exit(1)
    else:
        print(f"\n✓ All {report_data['completed']} chunk(s) generated successfully.")
        print(f"  Files in: {out_dir.relative_to(REPO_ROOT)}")
        print(f"  Next step: Hand off to Remotion (see skills/remotion/SKILL.md)")


if __name__ == "__main__":
    main()
