import sounddevice as sd
import numpy as np

duration = 3  # seconds
sample_rate = 44100  # Hz

# --- Test Speaker ---
print("Playing test tone...")
frequency = 440  # Hz (A4 note)
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
tone = 0.5 * np.sin(2 * np.pi * frequency * t)
sd.play(tone, samplerate=sample_rate)
sd.wait()

# --- Test Microphone ---
print("Recording from microphone...")
recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
sd.wait()
print("Recording complete.")

# --- Playback Recorded Audio ---
print("Playing back recorded audio...")
sd.play(recording, samplerate=sample_rate)
sd.wait()
print("Done.")
