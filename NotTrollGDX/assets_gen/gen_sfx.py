import math
import random
import struct
import wave

SR = 44100


def tone_samples(freq, dur, wave_type, gain, glide_to=None):
    n = int(SR * dur)
    out = [0.0] * n
    phase = 0.0
    for i in range(n):
        t = i / SR
        if glide_to is not None:
            # exponential frequency ramp from freq to glide_to over dur
            f = freq * (glide_to / freq) ** (t / dur)
        else:
            f = freq
        phase += f / SR
        ph = phase % 1.0
        if wave_type == 'square':
            s = 1.0 if ph < 0.5 else -1.0
        elif wave_type == 'sawtooth':
            s = 2.0 * ph - 1.0
        else:  # sine
            s = math.sin(2 * math.pi * phase)
        # exponential gain decay from `gain` to 0.001 over dur
        g = gain * ((0.001 / gain) ** (t / dur)) if gain > 0 else 0
        out[i] = s * g
    return out


def noise_samples(dur, gain):
    n = int(SR * dur)
    out = [0.0] * n
    for i in range(n):
        env = (1 - i / n)
        white = (random.random() * 2 - 1) * env
        t = i / SR
        g = gain * ((0.001 / gain) ** (t / dur)) if gain > 0 else 0
        out[i] = white * g
    return out


def mix(*tracks):
    length = max(len(t) for t in tracks)
    out = [0.0] * length
    for t in tracks:
        for i, v in enumerate(t):
            out[i] += v
    return out


def sequence(*parts_with_offsets):
    length = 0
    for samples, offset in parts_with_offsets:
        length = max(length, offset + len(samples))
    out = [0.0] * length
    for samples, offset in parts_with_offsets:
        for i, v in enumerate(samples):
            out[offset + i] += v
    return out


def write_wav(path, samples):
    peak = max(0.0001, max(abs(s) for s in samples))
    scale = min(1.0, 0.98 / peak)
    with wave.open(path, 'w') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(SR)
        frames = bytearray()
        for s in samples:
            v = max(-1.0, min(1.0, s * scale))
            frames += struct.pack('<h', int(v * 32767))
        f.writeframes(bytes(frames))


OUT = 'NotTrollGDX/assets/sfx/'

write_wav(OUT + 'jump.wav', tone_samples(420, 0.12, 'square', 0.12, 680))
write_wav(OUT + 'land.wav', tone_samples(160, 0.08, 'sine', 0.15, 90))
write_wav(OUT + 'death.wav', mix(
    tone_samples(300, 0.35, 'sawtooth', 0.18, 40),
    noise_samples(0.25, 0.15),
))
write_wav(OUT + 'goal.wav', sequence(
    (tone_samples(523, 0.1, 'square', 0.15, 523), 0),
    (tone_samples(659, 0.1, 'square', 0.15, 659), int(SR * 0.09)),
    (tone_samples(784, 0.22, 'square', 0.18, 784), int(SR * 0.18)),
))
write_wav(OUT + 'pop.wav', tone_samples(200, 0.08, 'square', 0.1, 90))
write_wav(OUT + 'crumble.wav', noise_samples(0.15, 0.12))
write_wav(OUT + 'boom.wav', mix(
    tone_samples(90, 0.3, 'sawtooth', 0.2, 40),
    noise_samples(0.3, 0.22),
))

print('SFX generated')
