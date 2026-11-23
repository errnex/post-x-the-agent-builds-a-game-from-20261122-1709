#!/usr/bin/env python3
"""34s chiptune bed: C-minor pentatonic arp + soft kick, 116 BPM, 22050 Hz mono."""
import math, struct, wave

SR = 22050
DUR = 34.0
BPM = 116
EIGHTH = 60.0 / BPM / 2

# C minor pentatonic: C3 Eb3 F3 G3 Bb3 C4 Eb4 F4 G4
SCALE = [130.81, 155.56, 174.61, 196.00, 233.08, 261.63, 311.13, 349.23, 392.00]
ARP = [0, 2, 4, 7, 5, 3, 4, 2, 0, 2, 4, 5, 7, 5, 4, 2]

n = int(SR * DUR)
out = [0.0] * n

def add_note(t0, freq, dur, vol, square=False):
    start = int(t0 * SR)
    end = min(n, int((t0 + dur) * SR))
    for i in range(start, end):
        t = (i - start) / SR
        env = min(1.0, t / 0.01) * math.exp(-3.0 * t / dur)
        if square:
            ph = (freq * t) % 1.0
            s = 1.0 if ph < 0.5 else -1.0
            s *= 0.6
        else:
            s = math.sin(2 * math.pi * freq * t)
        out[i] += vol * env * s

def add_kick(t0):
    start = int(t0 * SR)
    end = min(n, int((t0 + 0.22) * SR))
    for i in range(start, end):
        t = (i - start) / SR
        f = 120 - 380 * t
        env = math.exp(-14 * t)
        out[i] += 0.5 * env * math.sin(2 * math.pi * f * t)

steps = int(DUR / EIGHTH)
for s in range(steps):
    t0 = s * EIGHTH
    note = SCALE[ARP[s % len(ARP)]]
    add_note(t0, note, EIGHTH * 0.95, 0.16, square=(s % 4 == 2))
    if s % 2 == 0:
        add_kick(t0)

# gentle fade out over the last second
fade = int(SR * 1.0)
for i in range(fade):
    out[n - fade + i] *= (1.0 - i / fade)

with wave.open("audio.wav", "wb") as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(SR)
    frames = b"".join(struct.pack("<h", max(-32767, min(32767, int(v * 32767)))) for v in out)
    w.writeframes(frames)
print("audio.wav written", DUR, "s")
