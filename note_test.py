import pygame
import numpy as np
import scipy.io.wavfile as wf

pygame.mixer.init(size = 32)
samplerate = 44100

def generate_wave(hz, sineness, duration, vol):
    samples = int(duration * samplerate)

    if sineness == 0:
        buffer = np.sign(np.ceil(np.arange(samples) * hz / samplerate) - np.arange(samples) * hz / samplerate - 0.5).astype(np.float32)
    else:
        buffer = np.sin(2 * np.pi * np.arange(samples) * hz / samplerate).astype(np.float32)
        buffer = np.sign(buffer)*np.float_power(abs(buffer), sineness*np.ones(samples)).astype(np.float32)

    return buffer*vol

buffer = []
for x in np.arange(0, 1, 0.005):
    for y in generate_wave(300, x, 0.01, 0.02):
        buffer.append(y)

buffer = np.array(buffer).astype(np.float32)
sound = pygame.mixer.Sound(buffer)
sound.play()

wf.write('test.wav', samplerate, buffer)