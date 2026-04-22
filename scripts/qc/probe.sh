#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# probe.sh  —  Objective QC probe for a rendered video
#
# Usage:  bash scripts/qc/probe.sh <video.mp4> [output_dir]
#
# Outputs:
#   <output_dir>/qc.json        — machine-readable QC summary
#   <output_dir>/qc-report.txt  — human-readable pass/fail report (for Zimmer to read)
#
# Requires: ffprobe, ffmpeg (both in PATH)
#
# Zimmer reads qc.json and qc-report.txt after every render.
# No approval is valid without first running this script.
# ─────────────────────────────────────────────────────────────────────────────

set -euo pipefail

VIDEO="${1:-}"
OUT_DIR="${2:-scripts/qc}"

if [[ -z "$VIDEO" ]]; then
  echo "Usage: bash scripts/qc/probe.sh <video.mp4> [output_dir]"
  exit 1
fi

if [[ ! -f "$VIDEO" ]]; then
  echo "ERROR: File not found: $VIDEO"
  exit 1
fi

mkdir -p "$OUT_DIR"

QC_JSON="$OUT_DIR/qc.json"
QC_REPORT="$OUT_DIR/qc-report.txt"

echo "🔍 Probing: $VIDEO"
echo "   Output → $QC_JSON"
echo ""

# ── 1. ffprobe — codec, fps, duration, resolution ─────────────────────────────
echo "  [1/6] ffprobe: streams..."
PROBE_JSON=$(ffprobe -v quiet -print_format json -show_streams -show_format "$VIDEO" 2>/dev/null)

VIDEO_STREAM=$(echo "$PROBE_JSON" | python3 -c "
import json, sys
d = json.load(sys.stdin)
vs = [s for s in d.get('streams',[]) if s.get('codec_type')=='video']
print(json.dumps(vs[0] if vs else {}))
")

AUDIO_STREAM=$(echo "$PROBE_JSON" | python3 -c "
import json, sys
d = json.load(sys.stdin)
as_ = [s for s in d.get('streams',[]) if s.get('codec_type')=='audio']
print(json.dumps(as_[0] if as_ else {}))
")

FORMAT=$(echo "$PROBE_JSON" | python3 -c "
import json, sys
d = json.load(sys.stdin)
print(json.dumps(d.get('format',{})))
")

# ── 2. ebur128 — loudness ──────────────────────────────────────────────────────
echo "  [2/6] ebur128: loudness..."
EBUR_RAW=$(ffmpeg -i "$VIDEO" -filter:a ebur128=peak=true -f null - 2>&1 | tail -30 || true)
INTEGRATED=$(echo "$EBUR_RAW" | grep -o 'I:[[:space:]]*-\?[0-9.]*' | tail -1 | grep -o '\-\?[0-9.]*' || echo "N/A")
LOUDNESS_RANGE=$(echo "$EBUR_RAW" | grep -o 'LRA:[[:space:]]*[0-9.]*' | tail -1 | grep -o '[0-9.]*' || echo "N/A")
TRUE_PEAK=$(echo "$EBUR_RAW" | grep -o 'Peak:[[:space:]]*-\?[0-9.]*' | tail -1 | grep -o '\-\?[0-9.]*' || echo "N/A")

# ── 3. silencedetect — dead air ───────────────────────────────────────────────
echo "  [3/6] silencedetect: dead air..."
SILENCE_RAW=$(ffmpeg -i "$VIDEO" -af "silencedetect=noise=-35dB:d=0.3" -f null - 2>&1 | grep silence || true)
SILENCE_COUNT=$(echo "$SILENCE_RAW" | grep -c "silence_start" || echo "0")
SILENCE_EVENTS=$(echo "$SILENCE_RAW" | python3 -c "
import sys, re, json
lines = sys.stdin.read()
starts = re.findall(r'silence_start: ([0-9.]+)', lines)
ends = re.findall(r'silence_end: ([0-9.]+)', lines)
durs = re.findall(r'silence_duration: ([0-9.]+)', lines)
events = []
for i, s in enumerate(starts):
    e = {'start': float(s)}
    if i < len(ends): e['end'] = float(ends[i])
    if i < len(durs): e['duration'] = float(durs[i])
    events.append(e)
print(json.dumps(events))
" || echo "[]")

# ── 4. mpdecimate — duplicate frames (judder ratio) ───────────────────────────
echo "  [4/6] mpdecimate: duplicate frames..."
MPDEC_RAW=$(ffmpeg -i "$VIDEO" -vf mpdecimate -f null - 2>&1 | grep -c "drop" || echo "0")
TOTAL_FRAMES=$(echo "$VIDEO_STREAM" | python3 -c "
import json, sys
s = json.load(sys.stdin)
nb = s.get('nb_frames','')
if nb: print(nb)
else:
    dur = float(s.get('duration', 0) or 0)
    fr = s.get('r_frame_rate','30/1').split('/')
    fps = float(fr[0])/float(fr[1]) if len(fr)==2 else 30
    print(int(dur*fps))
" || echo "1")
JUDDER_RATIO=$(python3 -c "print(round($MPDEC_RAW / max(int('$TOTAL_FRAMES'),1), 4))" || echo "0")

# ── 5. scene cuts — timestamps ────────────────────────────────────────────────
echo "  [5/6] scene detect: cut timestamps..."
SCENE_RAW=$(ffmpeg -i "$VIDEO" -vf "select=gt(scene\,0.4),showinfo" -f null - 2>&1 | grep "pts_time" || true)
SCENE_TIMESTAMPS=$(echo "$SCENE_RAW" | python3 -c "
import sys, re, json
lines = sys.stdin.read()
ts = re.findall(r'pts_time:([0-9.]+)', lines)
print(json.dumps([float(t) for t in ts]))
" || echo "[]")

# ── 6. astats — audio clipping ────────────────────────────────────────────────
echo "  [6/6] astats: audio clipping..."
ASTATS_RAW=$(ffmpeg -i "$VIDEO" -af "astats=metadata=1:reset=1" -f null - 2>&1 | grep "Peak level" | tail -5 || true)
PEAK_DB=$(echo "$ASTATS_RAW" | grep -o '\-\?[0-9.]*' | sort -n | tail -1 || echo "N/A")

# ── Build qc.json ──────────────────────────────────────────────────────────────
echo ""
echo "  Building qc.json..."

python3 - <<PYEOF
import json, sys

video_stream = $VIDEO_STREAM
audio_stream = $AUDIO_STREAM
fmt = $FORMAT

# Extract key values
fps_raw = video_stream.get('r_frame_rate','0/1').split('/')
fps = round(float(fps_raw[0])/float(fps_raw[1]), 3) if len(fps_raw)==2 and float(fps_raw[1])>0 else 0
width = int(video_stream.get('width', 0))
height = int(video_stream.get('height', 0))
codec = video_stream.get('codec_name','unknown')
duration = float(fmt.get('duration', 0))
has_audio = bool(audio_stream)
integrated_lufs = '$INTEGRATED'
true_peak = '$TRUE_PEAK'
judder_ratio = $JUDDER_RATIO
silence_events = $SILENCE_EVENTS
scene_cuts = $SCENE_TIMESTAMPS
peak_db = '$PEAK_DB'

# Pass/Fail checks
checks = {}

# FPS check — warn if unusual (agents should verify against source)
checks['fps'] = {
    'value': fps,
    'note': 'Verify this matches source video fps (see skills/video-laws.md V1)',
    'status': 'info'
}

# Resolution
checks['resolution'] = {
    'value': f'{width}x{height}',
    'expected_reels': '1080x1920',
    'status': 'pass' if (width==1080 and height==1920) or (width==1080 and height==1080) else 'fail'
}

# Duration
checks['duration_seconds'] = {
    'value': round(duration, 2),
    'status': 'pass' if duration > 3 else 'fail',
    'note': 'Expected >3s'
}

# Loudness (target -14 LUFS for speech; -20 to -16 for pure BGM)
try:
    lufs_val = float(integrated_lufs)
    lufs_ok = -23 <= lufs_val <= -6
    lufs_status = 'pass' if lufs_ok else 'warn'
    lufs_note = 'OK' if lufs_ok else f'Integrated LUFS {lufs_val} is outside -23 to -6 range'
except:
    lufs_val = integrated_lufs
    lufs_status = 'warn'
    lufs_note = 'Could not parse LUFS value'
checks['loudness_lufs'] = {
    'integrated': lufs_val,
    'true_peak': true_peak,
    'status': lufs_status,
    'note': lufs_note
}

# Silence events
checks['silence_events'] = {
    'count': len(silence_events),
    'events': silence_events,
    'status': 'warn' if len(silence_events) > 5 else 'pass',
    'note': 'High silence count may indicate dead air between clips'
}

# Judder (duplicate frames ratio)
checks['judder_ratio'] = {
    'value': judder_ratio,
    'threshold': 0.15,
    'status': 'pass' if judder_ratio < 0.15 else 'fail',
    'note': f'Ratio {judder_ratio} — fail if >0.15 (indicates fps mismatch or encode issue)'
}

# Scene cuts
checks['scene_cuts'] = {
    'count': len(scene_cuts),
    'timestamps_seconds': scene_cuts,
    'status': 'info',
    'note': 'Use these timestamps in extract_frames.sh to pull QC frames'
}

# Audio presence
checks['has_audio'] = {
    'value': has_audio,
    'status': 'pass' if has_audio else 'warn',
    'note': 'No audio detected — expected for most formats'
}

# Clipping
try:
    peak = float(peak_db)
    clip_ok = peak < 0
    checks['audio_peak_db'] = {
        'value': peak,
        'status': 'pass' if clip_ok else 'fail',
        'note': 'Pass if peak < 0 dBFS (no clipping)'
    }
except:
    checks['audio_peak_db'] = {'value': peak_db, 'status': 'info'}

# Overall
all_statuses = [c.get('status','info') for c in checks.values()]
overall = 'fail' if 'fail' in all_statuses else ('warn' if 'warn' in all_statuses else 'pass')

output = {
    'file': '$VIDEO',
    'overall': overall,
    'codec': codec,
    'fps': fps,
    'resolution': f'{width}x{height}',
    'duration_seconds': round(duration, 2),
    'checks': checks
}

with open('$QC_JSON', 'w') as f:
    json.dump(output, f, indent=2)

print(json.dumps(output, indent=2))
PYEOF

# ── Build human-readable report ────────────────────────────────────────────────
python3 - <<PYEOF2
import json

with open('$QC_JSON') as f:
    d = json.load(f)

lines = []
lines.append("=" * 60)
lines.append(f"QC REPORT — {d['file']}")
lines.append("=" * 60)
lines.append(f"Overall: {d['overall'].upper()}")
lines.append(f"Codec:   {d['codec']}  |  FPS: {d['fps']}  |  {d['resolution']}  |  {d['duration_seconds']}s")
lines.append("")

for name, check in d['checks'].items():
    status = check.get('status','?').upper()
    marker = '✓' if status=='PASS' else ('⚠' if status=='WARN' else ('✗' if status=='FAIL' else 'ℹ'))
    note = check.get('note','')
    val = check.get('value', check.get('integrated', check.get('count', '')))
    lines.append(f"  {marker} [{status:4s}] {name}: {val}  {note}")

lines.append("")
lines.append("Next step: run scripts/qc/extract_frames.sh to pull visual frames for review.")
lines.append("=" * 60)

report = "\n".join(lines)
print(report)
with open('$QC_REPORT', 'w') as f:
    f.write(report + "\n")
PYEOF2

echo ""
echo "✅ QC probe complete."
echo "   Read: $QC_JSON"
echo "   Read: $QC_REPORT"
echo ""
