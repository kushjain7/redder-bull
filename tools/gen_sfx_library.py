#!/usr/bin/env python3
"""
Generate the full static SFX library for Redder Bull creatives.
Outputs to assets/static/sfx/ with organized subfolders.

Usage:
    python3 tools/gen_sfx_library.py

Requires: ffmpeg in PATH
"""

import subprocess, struct, math, random, os, sys

RATE = 44100

def write_wav(path: str, samples: list[float]):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    wav_path = path.replace(".mp3", ".wav")
    clipped = [max(-1.0, min(1.0, s)) for s in samples]
    data = struct.pack(f"<{len(clipped)}h", *[int(s * 32767) for s in clipped])
    with open(wav_path, "wb") as f:
        n = len(data)
        f.write(b"RIFF"); f.write(struct.pack("<I", 36 + n))
        f.write(b"WAVE"); f.write(b"fmt ")
        f.write(struct.pack("<IHHIIHH", 16, 1, 1, RATE, RATE * 2, 2, 16))
        f.write(b"data"); f.write(struct.pack("<I", n)); f.write(data)
    result = subprocess.run(
        ["ffmpeg", "-y", "-i", wav_path, "-b:a", "192k", path],
        capture_output=True
    )
    os.remove(wav_path)
    if result.returncode != 0:
        print(f"  ⚠ ffmpeg error for {path}: {result.stderr.decode()[:100]}")

def sine(freq, dur, vol=1.0, phase=0.0):
    n = int(RATE * dur)
    return [vol * math.sin(2 * math.pi * freq * i / RATE + phase) for i in range(n)]

def noise(dur, vol=1.0):
    n = int(RATE * dur)
    return [vol * (random.random() * 2 - 1) for _ in range(n)]

def env_adsr(samples, attack=0.01, decay=0.05, sustain=0.7, release=0.1):
    n = len(samples)
    a, d, r = int(attack * RATE), int(decay * RATE), int(release * RATE)
    s_len = n - a - d - r
    result = []
    for i, s in enumerate(samples):
        if i < a:
            result.append(s * (i / max(a, 1)))
        elif i < a + d:
            result.append(s * (1.0 - (1.0 - sustain) * ((i - a) / max(d, 1))))
        elif i < a + d + s_len:
            result.append(s * sustain)
        else:
            remaining = n - i
            result.append(s * sustain * (remaining / max(r, 1)))
    return result

def env_fade_out(samples, fade_frac=0.3):
    n = len(samples)
    fade_start = int(n * (1 - fade_frac))
    result = list(samples)
    for i in range(fade_start, n):
        result[i] *= (n - i) / (n - fade_start)
    return result

def env_fade_in(samples, fade_frac=0.15):
    n = len(samples)
    fade_end = int(n * fade_frac)
    result = list(samples)
    for i in range(fade_end):
        result[i] *= i / fade_end
    return result

def mix(*tracks):
    maxlen = max(len(t) for t in tracks)
    result = [0.0] * maxlen
    for t in tracks:
        for i, s in enumerate(t):
            result[i] += s
    return result

def normalize(samples, peak=0.85):
    m = max(abs(s) for s in samples) or 1
    return [s * peak / m for s in samples]

# ── TRANSITIONS ──────────────────────────────────────────────────────────────

def gen_whoosh_fast():
    """Fast, punchy left-to-right whoosh"""
    dur = 0.35
    n = int(RATE * dur)
    samples = []
    for i in range(n):
        t = i / RATE
        prog = i / n
        freq = 200 + 2800 * prog
        noise_s = (random.random() * 2 - 1) * 0.3
        tone_s = math.sin(2 * math.pi * freq * t) * 0.7
        vol = math.exp(-6 * prog)
        samples.append((noise_s + tone_s) * vol)
    return normalize(env_fade_out(samples, 0.25))

def gen_whoosh_soft():
    """Softer, airy whoosh"""
    dur = 0.5
    n = int(RATE * dur)
    samples = []
    for i in range(n):
        prog = i / n
        freq = 120 + 800 * prog
        noise_s = (random.random() * 2 - 1) * 0.6
        vol = math.sin(math.pi * prog) * math.exp(-2 * prog)
        # Low-pass-ish: attenuate high freqs
        lp = 1.0 - prog * 0.5
        samples.append(noise_s * vol * lp)
    return normalize(env_fade_out(samples, 0.3))

def gen_swoosh_down():
    """Downward swipe for closing/exit transitions"""
    dur = 0.4
    n = int(RATE * dur)
    samples = []
    for i in range(n):
        t = i / RATE
        prog = i / n
        freq = 1200 - 900 * prog
        noise_s = (random.random() * 2 - 1) * 0.4
        tone_s = math.sin(2 * math.pi * freq * t) * 0.6
        vol = (1 - prog) * math.exp(-3 * prog)
        samples.append((noise_s + tone_s) * vol)
    return normalize(samples)

def gen_swipe_right():
    """Clean digital swipe — UI-style"""
    dur = 0.25
    n = int(RATE * dur)
    samples = []
    for i in range(n):
        t = i / RATE
        prog = i / n
        freq = 400 + 3200 * (prog ** 0.5)
        vol = (1 - prog) ** 2
        samples.append(math.sin(2 * math.pi * freq * t) * vol * 0.8)
    return normalize(samples)

# ── IMPACTS ───────────────────────────────────────────────────────────────────

def gen_thud_low():
    """Low-frequency deep thud — mascot/element entry"""
    dur = 0.4
    n = int(RATE * dur)
    body = sine(60, dur, 0.8)
    click = [math.sin(2 * math.pi * 800 * i / RATE) * math.exp(-80 * i / RATE)
             for i in range(n)]
    sub = [math.sin(2 * math.pi * 40 * i / RATE) * math.exp(-12 * i / RATE) * 0.5
           for i in range(n)]
    combined = mix(body, click, sub)
    return normalize(env_adsr(combined, attack=0.003, decay=0.08, sustain=0.1, release=0.25))

def gen_punch_mid():
    """Mid-range punch — for text/CTA moments"""
    dur = 0.3
    n = int(RATE * dur)
    body = [math.sin(2 * math.pi * 180 * i / RATE) * math.exp(-20 * i / RATE) * 0.7
            for i in range(n)]
    snap = [math.sin(2 * math.pi * 1200 * i / RATE) * math.exp(-120 * i / RATE) * 0.5
            for i in range(n)]
    combined = mix(body, snap)
    return normalize(env_fade_out(combined, 0.2))

def gen_impact_hard():
    """Hard cinematic impact — for boss moments, big reveals"""
    dur = 0.6
    n = int(RATE * dur)
    sub = [math.sin(2 * math.pi * 35 * i / RATE) * math.exp(-8 * i / RATE) * 0.9
           for i in range(n)]
    mid = [math.sin(2 * math.pi * 120 * i / RATE) * math.exp(-15 * i / RATE) * 0.6
           for i in range(n)]
    noise_burst = [(random.random() * 2 - 1) * math.exp(-30 * i / RATE) * 0.4
                   for i in range(n)]
    combined = mix(sub, mid, noise_burst)
    return normalize(env_fade_out(combined, 0.4))

def gen_snare_accent():
    """Tight snare accent — for stat/number reveals"""
    dur = 0.2
    n = int(RATE * dur)
    noise_s = [(random.random() * 2 - 1) * math.exp(-35 * i / RATE) * 0.7
               for i in range(n)]
    tone = [math.sin(2 * math.pi * 200 * i / RATE) * math.exp(-50 * i / RATE) * 0.4
            for i in range(n)]
    combined = mix(noise_s, tone)
    return normalize(combined)

def gen_pop_soft():
    """Soft pop — for element appearances (non-harsh)"""
    dur = 0.15
    n = int(RATE * dur)
    samples = [math.sin(2 * math.pi * 300 * i / RATE) * math.exp(-60 * i / RATE) * 0.6
               for i in range(n)]
    return normalize(env_fade_out(samples, 0.3))

# ── RISERS ────────────────────────────────────────────────────────────────────

def gen_riser_cinematic():
    """Long cinematic riser — builds over 2.5s"""
    dur = 2.5
    n = int(RATE * dur)
    samples = []
    for i in range(n):
        t = i / RATE
        prog = i / n
        # Two harmonics rising
        f1 = 60 + 400 * (prog ** 1.5)
        f2 = 120 + 800 * (prog ** 1.5)
        noise_s = (random.random() * 2 - 1) * 0.15
        tone = (math.sin(2 * math.pi * f1 * t) * 0.5 +
                math.sin(2 * math.pi * f2 * t) * 0.3)
        vol = prog ** 0.8
        samples.append((tone + noise_s) * vol)
    return normalize(env_fade_in(env_fade_out(samples, 0.05), 0.1))

def gen_riser_electronic():
    """Electronic riser — 1.5s, synth-style"""
    dur = 1.5
    n = int(RATE * dur)
    samples = []
    for i in range(n):
        t = i / RATE
        prog = i / n
        freq = 100 + 1200 * prog
        saw = sum(math.sin(2 * math.pi * freq * k * t) / k for k in range(1, 6))
        noise_s = (random.random() * 2 - 1) * 0.1
        vol = prog ** 0.6
        samples.append((saw * 0.3 + noise_s) * vol)
    return normalize(env_fade_in(env_fade_out(samples, 0.05), 0.08))

def gen_riser_short():
    """Short 0.8s riser — for quick transitions"""
    dur = 0.8
    n = int(RATE * dur)
    samples = []
    for i in range(n):
        t = i / RATE
        prog = i / n
        freq = 200 + 600 * prog
        noise_s = (random.random() * 2 - 1) * 0.3 * prog
        tone = math.sin(2 * math.pi * freq * t) * (1 - 0.5 * prog)
        vol = prog * (1 - prog * 0.3)
        samples.append((tone + noise_s) * vol)
    return normalize(env_fade_out(samples, 0.05))

def gen_bass_swell():
    """Deep bass swell — for boss/power moments"""
    dur = 2.0
    n = int(RATE * dur)
    samples = []
    for i in range(n):
        t = i / RATE
        prog = i / n
        sub = math.sin(2 * math.pi * (30 + 80 * prog) * t) * 0.6
        mid = math.sin(2 * math.pi * (60 + 120 * prog) * t) * 0.3
        noise_s = (random.random() * 2 - 1) * 0.1 * prog
        vol = prog ** 0.5 * math.exp(-1.5 * max(0, prog - 0.7))
        samples.append((sub + mid + noise_s) * vol)
    return normalize(env_fade_in(samples, 0.05))

# ── AMBIENCE ──────────────────────────────────────────────────────────────────

def gen_tech_hum():
    """Subtle tech/server hum — for tech/coding scenes"""
    dur = 4.0
    n = int(RATE * dur)
    samples = []
    for i in range(n):
        t = i / RATE
        hum = (math.sin(2 * math.pi * 60 * t) * 0.3 +
               math.sin(2 * math.pi * 120 * t) * 0.15 +
               math.sin(2 * math.pi * 180 * t) * 0.07)
        noise_s = (random.random() * 2 - 1) * 0.03
        samples.append(hum + noise_s)
    return normalize(env_fade_in(env_fade_out(samples, 0.1), 0.1), peak=0.3)

def gen_city_ambience():
    """Light city background — for outdoor/street product scenes"""
    dur = 4.0
    n = int(RATE * dur)
    samples = []
    for i in range(n):
        # Band-limited noise + low hum
        noise_s = (random.random() * 2 - 1) * 0.15
        rumble = math.sin(2 * math.pi * 80 * i / RATE) * 0.1
        samples.append(noise_s + rumble)
    return normalize(env_fade_in(env_fade_out(samples, 0.15), 0.15), peak=0.25)

# ── UI ────────────────────────────────────────────────────────────────────────

def gen_typing_fast():
    """Fast keyboard typing — for terminal/code scenes"""
    dur = 2.0
    n = int(RATE * dur)
    samples = [0.0] * n
    bpm = 280
    beat = int(RATE * 60 / bpm)
    for beat_i in range(int(n / beat)):
        if random.random() > 0.25:
            pos = beat_i * beat + random.randint(-beat // 6, beat // 6)
            for j in range(min(int(RATE * 0.04), n - pos)):
                if pos + j < n:
                    key_click = math.sin(2 * math.pi * (800 + random.randint(-200, 200)) * j / RATE)
                    samples[pos + j] += key_click * math.exp(-80 * j / RATE) * 0.4
    return normalize(env_fade_in(env_fade_out(samples, 0.1), 0.05), peak=0.6)

def gen_typing_slow():
    """Slow deliberate typing — for text-on-screen typewriter effects"""
    dur = 2.0
    n = int(RATE * dur)
    samples = [0.0] * n
    bpm = 120
    beat = int(RATE * 60 / bpm)
    for beat_i in range(int(n / beat)):
        if random.random() > 0.3:
            pos = beat_i * beat + random.randint(-beat // 8, beat // 8)
            for j in range(min(int(RATE * 0.06), n - pos)):
                if pos + j < n:
                    click = math.sin(2 * math.pi * (600 + random.randint(-100, 100)) * j / RATE)
                    samples[pos + j] += click * math.exp(-60 * j / RATE) * 0.45
    return normalize(env_fade_in(env_fade_out(samples, 0.12), 0.05), peak=0.55)

def gen_notification():
    """Notification chime — for success/completion moments"""
    dur = 0.5
    freqs = [880, 1108, 1318]
    samples = [0.0] * int(RATE * dur)
    for k, freq in enumerate(freqs):
        start = int(k * RATE * 0.12)
        tone_dur = 0.25
        n_tone = int(RATE * tone_dur)
        for j in range(n_tone):
            if start + j < len(samples):
                samples[start + j] += (math.sin(2 * math.pi * freq * j / RATE) *
                                       math.exp(-8 * j / RATE) * 0.35)
    return normalize(env_fade_out(samples, 0.2))

def gen_click_ui():
    """Clean UI click — for button/element appear"""
    dur = 0.1
    n = int(RATE * dur)
    samples = [math.sin(2 * math.pi * 1000 * i / RATE) * math.exp(-100 * i / RATE) * 0.5
               for i in range(n)]
    return normalize(samples)


# ── MAIN ──────────────────────────────────────────────────────────────────────

BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "assets", "static", "sfx")

SFX_MAP = {
    # Transitions
    f"{BASE}/transitions/whoosh-fast-01.mp3":       gen_whoosh_fast,
    f"{BASE}/transitions/whoosh-soft-01.mp3":       gen_whoosh_soft,
    f"{BASE}/transitions/swoosh-down-01.mp3":       gen_swoosh_down,
    f"{BASE}/transitions/swipe-right-01.mp3":       gen_swipe_right,
    # Impacts
    f"{BASE}/impacts/thud-low-01.mp3":              gen_thud_low,
    f"{BASE}/impacts/punch-mid-01.mp3":             gen_punch_mid,
    f"{BASE}/impacts/impact-hard-01.mp3":           gen_impact_hard,
    f"{BASE}/impacts/snare-accent-01.mp3":          gen_snare_accent,
    f"{BASE}/impacts/pop-soft-01.mp3":              gen_pop_soft,
    # Risers
    f"{BASE}/risers/riser-cinematic-01.mp3":        gen_riser_cinematic,
    f"{BASE}/risers/riser-electronic-01.mp3":       gen_riser_electronic,
    f"{BASE}/risers/riser-short-01.mp3":            gen_riser_short,
    f"{BASE}/risers/bass-swell-01.mp3":             gen_bass_swell,
    # Ambience
    f"{BASE}/ambience/tech-hum-01.mp3":             gen_tech_hum,
    f"{BASE}/ambience/city-ambience-01.mp3":        gen_city_ambience,
    # UI
    f"{BASE}/ui/typing-fast-01.mp3":                gen_typing_fast,
    f"{BASE}/ui/typing-slow-01.mp3":                gen_typing_slow,
    f"{BASE}/ui/notification-01.mp3":               gen_notification,
    f"{BASE}/ui/click-ui-01.mp3":                   gen_click_ui,
}

if __name__ == "__main__":
    print(f"\n🎵 Generating SFX library → {BASE}\n")
    for path, fn in SFX_MAP.items():
        name = os.path.relpath(path, BASE)
        print(f"  Generating {name}...", end=" ", flush=True)
        samples = fn()
        write_wav(path, samples)
        size_kb = os.path.getsize(path) // 1024
        print(f"✓  ({size_kb}KB)")
    print(f"\n✅ Done — {len(SFX_MAP)} SFX files generated.\n")
