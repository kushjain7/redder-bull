"""
Generate all audio assets for the Agency Intro Video.
Run once: python3 gen_audio.py
Produces: bgm.mp3, sfx-whoosh.mp3, sfx-pop.mp3, sfx-typing.mp3, sfx-boss.mp3
"""
import wave
import array
import math
import subprocess
import os

SR = 44100

def write_wav(filename, samples):
    data = array.array('h', [max(-32767, min(32767, int(s * 32767))) for s in samples])
    with wave.open(filename, 'wb') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(SR)
        f.writeframes(data.tobytes())

def to_mp3(wav, mp3):
    subprocess.run(
        ['/opt/homebrew/bin/ffmpeg', '-y', '-i', wav, '-c:a', 'libmp3lame', '-b:a', '192k', mp3],
        capture_output=True
    )
    os.remove(wav)
    print(f'  -> {mp3}')

# ── 1. BGM: Electronic ambient beat (52s, 120 BPM) ───────────────────────────
print('Generating BGM...')
DUR = 55.0
N = int(SR * DUR)
BPM = 120.0
beat = 60.0 / BPM  # 0.5s

bgm = []
for i in range(N):
    t = i / SR
    b  = t % beat          # 0..0.5  (full beat cycle)
    b8 = t % (beat / 4)    # 0..0.125 (16th note)

    # Kick drum — punchy thud at start of each beat
    kick = 0.38 * math.sin(2 * math.pi * 58 * b) * math.exp(-22 * b) * (1 if b < 0.11 else 0)

    # Snare accent — every 2 beats (on the 2 and 4)
    b2 = t % (beat * 2)
    snare = 0.12 * math.sin(2 * math.pi * 300 * b2) * math.exp(-35 * (b2 - beat)) * (1 if b2 > beat - 0.01 and b2 < beat + 0.12 else 0)

    # Hi-hat — every 16th note, quiet
    hh = 0.03 * math.sin(2 * math.pi * 8500 * t) * math.exp(-180 * b8) * (1 if b8 < 0.015 else 0)

    # Sub bass — sustained with beat-sync pumping
    duck = max(0, 1 - kick * 3)   # sidechained feel
    bass = 0.14 * math.sin(2 * math.pi * 55 * t) * (0.6 + 0.4 * duck)

    # Chord pad — Am: A3 220Hz, C4 261Hz, E4 330Hz — slow tremolo
    trem = 0.5 + 0.5 * math.sin(2 * math.pi * 0.45 * t)
    pad  = trem * (
        0.055 * math.sin(2 * math.pi * 220  * t) +
        0.045 * math.sin(2 * math.pi * 261.6 * t) +
        0.040 * math.sin(2 * math.pi * 329.6 * t)
    )

    # Synth arp — Am pentatonic: A4(440) C5(523) E5(659) G5(784) A5(880)
    arp_notes = [440.0, 523.25, 659.25, 783.99]
    arp_period = beat / 4
    arp_idx  = int(t / arp_period) % len(arp_notes)
    bp       = t % arp_period
    arp_freq = arp_notes[arp_idx]
    arp = 0.06 * math.sin(2 * math.pi * arp_freq * t) * math.exp(-25 * bp) * (1 if bp < 0.06 else 0)

    # High shimmer — octave above arp, very quiet
    shimmer = 0.02 * math.sin(2 * math.pi * arp_freq * 2 * t) * math.exp(-40 * bp) * (1 if bp < 0.04 else 0)

    sample = kick + snare + hh + bass + pad + arp + shimmer

    # Fade in/out
    fade = 1.0
    if i < SR * 2.5: fade = i / (SR * 2.5)
    if i > N - SR * 4: fade = (N - i) / (SR * 4)

    bgm.append(max(-1.0, min(1.0, sample * fade * 0.88)))

write_wav('bgm.wav', bgm)
to_mp3('bgm.wav', 'bgm.mp3')

# ── 2. Whoosh — cinematic scene transition ────────────────────────────────────
print('Generating sfx-whoosh...')
N = int(SR * 0.7)
whoosh = []
for i in range(N):
    t = i / SR
    phase = 2 * math.pi * (180 * t + 2800 * t * t)
    amp = 0.45 * math.exp(-7 * (t - 0.18) ** 2)
    whoosh.append(amp * math.sin(phase))
write_wav('sfx-whoosh.wav', whoosh)
to_mp3('sfx-whoosh.wav', 'sfx-whoosh.mp3')

# ── 3. Pop — element appear (mascot entrance, text pop-in) ───────────────────
print('Generating sfx-pop...')
N = int(SR * 0.25)
pop = []
for i in range(N):
    t = i / SR
    freq = 1100 - 500 * t
    sample = 0.32 * math.sin(2 * math.pi * (1100 * t - 250 * t * t)) * math.exp(-22 * t)
    sample += 0.08 * math.sin(2 * math.pi * freq * 2 * t) * math.exp(-30 * t)
    pop.append(sample)
write_wav('sfx-pop.wav', pop)
to_mp3('sfx-pop.wav', 'sfx-pop.mp3')

# ── 4. Typing — mechanical keyboard loop (2s) ─────────────────────────────────
print('Generating sfx-typing...')
N = int(SR * 2.0)
typing = []
# Randomish click timings (manually seeded for consistency)
click_offsets = [0, 0.10, 0.21, 0.29, 0.40, 0.52, 0.60, 0.71,
                 0.83, 0.91, 1.02, 1.11, 1.22, 1.32, 1.41, 1.53,
                 1.62, 1.73, 1.81, 1.91]
for i in range(N):
    t = i / SR
    sample = 0.0
    for off in click_offsets:
        dt = t - off
        if 0 < dt < 0.025:
            freq_var = 2800 + (off * 300) % 800
            sample += 0.18 * math.sin(2 * math.pi * freq_var * dt) * math.exp(-350 * dt)
    typing.append(max(-1.0, min(1.0, sample)))
write_wav('sfx-typing.wav', typing)
to_mp3('sfx-typing.wav', 'sfx-typing.mp3')

# ── 5. Boss chord — Zimmer entrance (power chord + sub hit) ──────────────────
print('Generating sfx-boss...')
N = int(SR * 1.8)
boss = []
for i in range(N):
    t = i / SR
    env = math.exp(-1.2 * t) * (0.7 + 0.3 * math.sin(2 * math.pi * 3 * t))
    # E minor power chord
    chord = (
        0.18 * math.sin(2 * math.pi * 82  * t) +  # E2
        0.14 * math.sin(2 * math.pi * 164 * t) +  # E3
        0.10 * math.sin(2 * math.pi * 247 * t) +  # B3
        0.07 * math.sin(2 * math.pi * 329 * t)    # E4
    )
    # Sub bass hit at the start
    sub_hit = 0.25 * math.sin(2 * math.pi * 55 * t) * math.exp(-5 * t)
    boss.append(max(-1.0, min(1.0, (chord + sub_hit) * env)))
write_wav('sfx-boss.wav', boss)
to_mp3('sfx-boss.wav', 'sfx-boss.mp3')

print('\nAll audio files generated successfully.')
