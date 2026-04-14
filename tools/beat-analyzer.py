#!/usr/bin/env python3
"""
Beat Analyzer — Reusable music analysis tool for Remotion video sync.

Usage:
    python3 tools/beat-analyzer.py <path-to-mp3> [--fps 30] [--video-duration 50]

Output:
    - Song duration
    - Beat drop timestamp (when energy first jumps significantly)
    - Estimated BPM
    - Phrase cycle length (how often the musical pattern repeats)
    - Recommended Remotion `startFrom` offset for common sync points

This tool converts MP3 → WAV (temp), analyzes energy envelope,
finds the beat drop, estimates BPM via autocorrelation, and
calculates phrase boundaries.

Requires: ffmpeg (for MP3 → WAV conversion)
"""

import subprocess
import wave
import array
import math
import os
import sys
import argparse
import json
import shutil
import tempfile

# ─── Config ───────────────────────────────────────────────────────────────────

# Resolve ffmpeg from PATH first; fall back to the Homebrew location on macOS.
FFMPEG = shutil.which('ffmpeg') or '/opt/homebrew/bin/ffmpeg'
ANALYSIS_SR = 22050  # downsample to 22kHz for faster processing


def mp3_to_wav(mp3_path: str, wav_path: str) -> None:
    subprocess.run(
        [FFMPEG, '-y', '-i', mp3_path,
         '-acodec', 'pcm_s16le', '-ar', str(ANALYSIS_SR), '-ac', '1', wav_path],
        capture_output=True, check=True,
    )


def read_wav(wav_path: str) -> tuple[list[float], int, float]:
    with wave.open(wav_path, 'rb') as w:
        nf = w.getnframes()
        sr = w.getframerate()
        raw = w.readframes(nf)
    samples = [s / 32768.0 for s in array.array('h', raw)]
    duration = nf / sr
    return samples, sr, duration


def compute_rms(samples: list[float], sr: int,
                window_s: float = 0.5, step_s: float = 0.1) -> list[tuple[float, float]]:
    """Compute a sliding-window RMS envelope using prefix sums — O(n) time."""
    win = int(sr * window_s)
    step = int(sr * step_s)
    n = len(samples)

    if win <= 0 or n < win:
        return []

    # Build prefix-sum of squares once — avoids re-summing each window.
    prefix = [0.0] * (n + 1)
    for i, x in enumerate(samples):
        prefix[i + 1] = prefix[i] + x * x

    rms = []
    for i in range(0, n - win, step):
        window_sum = prefix[i + win] - prefix[i]
        v = math.sqrt(window_sum / win)
        rms.append((i / sr, v))
    return rms


def find_beat_drop(rms: list[tuple[float, float]],
                   min_time: float = 2.0) -> tuple[float, float]:
    """Find the first significant energy jump after min_time seconds.

    Uses a sliding window approach: compares short-term energy (1s) against
    the energy of the preceding 3s window. A "drop" is when short-term
    energy is 2.5× the preceding window's energy — catching both sudden
    drops and gradual builds that culminate in a clear energy jump.
    """
    max_rms = max(v for _, v in rms)
    if max_rms == 0:
        return 0.0, 0.0

    step_s = rms[1][0] - rms[0][0] if len(rms) > 1 else 0.1
    window_pre = int(3.0 / step_s)   # 3-second lookback
    window_post = int(1.0 / step_s)  # 1-second lookahead

    best_ratio = 0.0
    best_time = 0.0
    best_energy = 0.0

    for i in range(window_pre, len(rms) - window_post):
        t = rms[i][0]
        if t < min_time:
            continue

        pre_avg = sum(rms[j][1] for j in range(i - window_pre, i)) / window_pre
        post_avg = sum(rms[j][1] for j in range(i, i + window_post)) / window_post

        if pre_avg > 0 and post_avg > max_rms * 0.3:
            ratio = post_avg / pre_avg
            if ratio > best_ratio:
                best_ratio = ratio
                best_time = t
                best_energy = post_avg

    if best_ratio > 1.5:
        return best_time, best_energy

    # Fallback: find where energy first exceeds 50% of max
    for t, v in rms:
        if t >= min_time and v > max_rms * 0.5:
            return t, v

    return 0.0, 0.0


def estimate_bpm(samples: list[float], sr: int,
                 start_s: float = 0.0, duration_s: float = 30.0) -> float:
    """Estimate BPM using onset detection autocorrelation."""
    start_i = int(start_s * sr)
    end_i = min(len(samples), int((start_s + duration_s) * sr))
    seg = samples[start_i:end_i]

    if len(seg) < sr * 4:
        return 0.0

    # Compute onset strength: RMS difference in small windows
    win = int(sr * 0.02)  # 20ms windows
    step = int(sr * 0.01)  # 10ms steps
    onset = []
    prev_rms = 0.0
    for i in range(0, len(seg) - win, step):
        chunk = seg[i:i + win]
        r = math.sqrt(sum(x * x for x in chunk) / len(chunk))
        diff = max(0, r - prev_rms)
        onset.append(diff)
        prev_rms = r

    if len(onset) < 100:
        return 0.0

    # Autocorrelation on onset signal
    mean_o = sum(onset) / len(onset)
    centered = [x - mean_o for x in onset]
    norm = sum(x * x for x in centered)
    if norm == 0:
        return 0.0

    # Search lags corresponding to 60-180 BPM
    step_s = 0.01
    best_r = -1.0
    best_bpm = 0       # initialised here — avoids UnboundLocalError when no lag matches
    for bpm in range(60, 181):
        lag_s = 60.0 / bpm
        lag_steps = int(lag_s / step_s)
        if lag_steps >= len(centered):
            continue
        corr = sum(centered[i] * centered[i + lag_steps]
                   for i in range(len(centered) - lag_steps))
        r = corr / norm
        if r > best_r:
            best_r = r
            best_bpm = bpm

    return float(best_bpm) if best_r > 0.05 else 0.0


def find_phrase_cycle(rms: list[tuple[float, float]],
                      drop_time: float,
                      search_duration: float = 60.0) -> float:
    """Find the phrase/cycle length after the beat drop using autocorrelation on RMS envelope."""
    post_rms = [v for t, v in rms if drop_time <= t <= drop_time + search_duration]

    if len(post_rms) < 60:
        return 0.0

    mean = sum(post_rms) / len(post_rms)
    centered = [x - mean for x in post_rms]
    norm = sum(x * x for x in centered)
    if norm == 0:
        return 0.0

    step_s = 0.1  # RMS step
    best_r = -1.0
    best_lag_s = 0.0

    # Search for cycles between 4s and 20s
    for lag_steps in range(int(4 / step_s), int(20 / step_s)):
        if lag_steps >= len(centered):
            break
        corr = sum(centered[i] * centered[i + lag_steps]
                   for i in range(len(centered) - lag_steps))
        r = corr / norm
        if r > best_r:
            best_r = r
            best_lag_s = lag_steps * step_s

    return best_lag_s if best_r > 0.02 else 0.0


def compute_start_from(drop_time: float, video_drop_time: float, fps: int) -> int:
    """Calculate Remotion startFrom so song's beat drop aligns with video_drop_time."""
    song_start = drop_time - video_drop_time
    if song_start < 0:
        song_start = 0
    return int(song_start * fps)


def main():
    parser = argparse.ArgumentParser(description='Beat Analyzer for Remotion video sync')
    parser.add_argument('mp3_path', help='Path to the MP3 file to analyze')
    parser.add_argument('--fps', type=int, default=30, help='Video frame rate (default: 30)')
    parser.add_argument('--video-duration', type=float, default=0,
                        help='Target video duration in seconds (for scene planning)')
    parser.add_argument('--drop-at-video-second', type=float, default=6.0,
                        help='When the beat drop should land in the video (default: 6.0s)')
    parser.add_argument('--json', action='store_true', help='Output as compact JSON')
    args = parser.parse_args()

    if not os.path.exists(args.mp3_path):
        print(f'Error: File not found: {args.mp3_path}', file=sys.stderr)
        sys.exit(1)

    # Use a process-unique temp file to avoid collisions under parallel runs.
    tmp_fd, wav_path = tempfile.mkstemp(suffix='.wav')
    os.close(tmp_fd)
    try:
        mp3_to_wav(args.mp3_path, wav_path)
        samples, sr, duration = read_wav(wav_path)
    finally:
        if os.path.exists(wav_path):
            os.remove(wav_path)

    rms = compute_rms(samples, sr)
    drop_time, drop_energy = find_beat_drop(rms)
    bpm = estimate_bpm(samples, sr, start_s=drop_time, duration_s=30.0)
    phrase_cycle = find_phrase_cycle(rms, drop_time)
    start_from = compute_start_from(drop_time, args.drop_at_video_second, args.fps)

    # Beat period
    beat_period = 60.0 / bpm if bpm > 0 else 0.0
    phrase_frames = int(phrase_cycle * args.fps) if phrase_cycle > 0 else 0

    result = {
        'file': os.path.basename(args.mp3_path),
        'duration_s': round(duration, 2),
        'beat_drop_s': round(drop_time, 2),
        'bpm': round(bpm, 1),
        'beat_period_s': round(beat_period, 3),
        'phrase_cycle_s': round(phrase_cycle, 1),
        'phrase_cycle_frames': phrase_frames,
        'recommended_start_from': start_from,
        'drop_at_video_second': args.drop_at_video_second,
        'fps': args.fps,
    }

    if args.json:
        # Compact (no whitespace) — token-efficient for LLM / scripted consumption.
        print(json.dumps(result, separators=(',', ':')))
    else:
        print(f'''
╔══════════════════════════════════════════════════════════════╗
║                    BEAT ANALYSIS REPORT                      ║
╠══════════════════════════════════════════════════════════════╣
║  File:              {result["file"]:<39} ║
║  Duration:          {result["duration_s"]}s{" " * (36 - len(str(result["duration_s"])))} ║
║                                                              ║
║  Beat Drop:         {result["beat_drop_s"]}s (song timestamp){" " * max(0, 20 - len(str(result["beat_drop_s"])))} ║
║  BPM:               {result["bpm"]}{" " * (38 - len(str(result["bpm"])))} ║
║  Beat Period:       {result["beat_period_s"]}s{" " * (36 - len(str(result["beat_period_s"])))} ║
║  Phrase Cycle:      {result["phrase_cycle_s"]}s = {result["phrase_cycle_frames"]} frames{" " * max(0, 24 - len(str(result["phrase_cycle_s"])) - len(str(result["phrase_cycle_frames"])))} ║
║                                                              ║
║  ── Remotion Sync ─────────────────────────────────────────  ║
║  startFrom:         {result["recommended_start_from"]} frames{" " * max(0, 30 - len(str(result["recommended_start_from"])))} ║
║  (Drop lands at video second {result["drop_at_video_second"]}){" " * max(0, 28 - len(str(result["drop_at_video_second"])))} ║
║  Scene duration:    {result["phrase_cycle_frames"]} frames ({result["phrase_cycle_s"]}s) per phrase{" " * max(0, 14 - len(str(result["phrase_cycle_frames"])) - len(str(result["phrase_cycle_s"])))} ║
╚══════════════════════════════════════════════════════════════╝

Usage in Remotion:
  <Audio
    src={{staticFile('{result["file"]}')}}
    volume={{0.28}}
    startFrom={{{result["recommended_start_from"]}}}
  />

  // Each major scene = {result["phrase_cycle_frames"]} frames ({result["phrase_cycle_s"]}s)
  // Beat drop aligns with video second {result["drop_at_video_second"]}
''')

if __name__ == '__main__':
    main()
