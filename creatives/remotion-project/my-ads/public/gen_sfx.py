"""
Regenerate SFX: softer pop + new boss-incoming + text-impact.
Run: python3 gen_sfx.py
"""
import wave, array, math, subprocess, os

SR = 44100

def write_wav(fn, samples):
    data = array.array('h', [max(-32767, min(32767, int(s * 32767))) for s in samples])
    with wave.open(fn, 'wb') as f:
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(SR); f.writeframes(data.tobytes())

def to_mp3(wav, mp3):
    subprocess.run(['/opt/homebrew/bin/ffmpeg', '-y', '-i', wav, '-c:a', 'libmp3lame', '-b:a', '192k', mp3], capture_output=True)
    os.remove(wav)
    print(f'  -> {mp3}')

# ── 1. Soft mascot appear — low thud + shimmer (replace old high-freq pop) ────
print('Generating sfx-pop (softer)...')
N = int(SR * 0.45)
pop = []
for i in range(N):
    t = i / SR
    thud    = 0.40 * math.sin(2 * math.pi * 100 * t) * math.exp(-9 * t)
    body    = 0.20 * math.sin(2 * math.pi * 220 * t) * math.exp(-14 * t)
    sparkle = 0.08 * math.sin(2 * math.pi * 600 * t) * math.exp(-30 * t)
    pop.append(max(-1.0, min(1.0, thud + body + sparkle)))
write_wav('sfx-pop.wav', pop)
to_mp3('sfx-pop.wav', 'sfx-pop.mp3')

# ── 2. Boss incoming — deep bass swell building 2.5s, crescendo for Zimmer ───
print('Generating sfx-boss-incoming...')
N = int(SR * 2.6)
boss_in = []
for i in range(N):
    t = i / SR
    intensity = (t / 2.2) ** 2   # accelerating build
    # Sub bass rumble (55 Hz) growing louder
    sub = 0.28 * intensity * math.sin(2 * math.pi * 55 * t)
    # Orchestra swell: rising pitch string hit
    sweep = 0.18 * intensity * math.sin(2 * math.pi * (90 + 60 * t) * t) * (0.5 + 0.5 * math.sin(2 * math.pi * 1.5 * t))
    # Tremolo tension string
    trem_freq = 130 + 30 * (t / 2.6)
    trem = 0.12 * intensity * math.sin(2 * math.pi * trem_freq * t) * (0.5 + 0.5 * math.sin(2 * math.pi * 8 * t))
    # Sharp impact at t=2.3s
    imp = 0.0
    if t > 2.25:
        it = t - 2.25
        imp = 0.5 * math.sin(2 * math.pi * 82 * it) * math.exp(-7 * it)
        imp += 0.3 * math.sin(2 * math.pi * 220 * it) * math.exp(-9 * it)
    # Fade in
    fade_in = min(1.0, t / 0.3)
    boss_in.append(max(-1.0, min(1.0, (sub + sweep + trem + imp) * fade_in)))
write_wav('sfx-boss-incoming.wav', boss_in)
to_mp3('sfx-boss-incoming.wav', 'sfx-boss-incoming.mp3')

# ── 3. Text impact — sharp accent beat for key moments ("I'm the boss" etc.) ─
print('Generating sfx-text-impact...')
N = int(SR * 0.4)
impact = []
for i in range(N):
    t = i / SR
    # Tight snare-style hit: noise burst + tone
    click = 0.45 * math.sin(2 * math.pi * 180 * t) * math.exp(-32 * t)
    snap  = 0.25 * math.sin(2 * math.pi * 500 * t) * math.exp(-50 * t)
    tail  = 0.12 * math.sin(2 * math.pi * 1400 * t) * math.exp(-120 * t)
    impact.append(max(-1.0, min(1.0, click + snap + tail)))
write_wav('sfx-text-impact.wav', impact)
to_mp3('sfx-text-impact.wav', 'sfx-text-impact.mp3')

print('\nSFX regenerated.')
