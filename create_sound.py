import numpy as np
from scipy.io import wavfile

# Create a simple "pop" sound
sample_rate = 44100
duration = 0.1
t = np.linspace(0, duration, int(sample_rate * duration))
frequency = 440
amplitude = np.iinfo(np.int16).max

# Create a simple sine wave with decay
audio = amplitude * np.sin(2 * np.pi * frequency * t) * np.exp(-5 * t)
audio = audio.astype(np.int16)

# Save the sound
wavfile.write('eat.wav', sample_rate, audio) 