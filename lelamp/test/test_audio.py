import sounddevice as sd
import numpy as np

def get_seeed_device(output=True):
    """Return the first Seeed device index for output or input."""
    seeed_devices = [
        (i, d) for i, d in enumerate(sd.query_devices())
        if "seeed" in d['name'].lower()
    ]
    for i, d in seeed_devices:
        if output and d['max_output_channels'] > 0:
            return i
        if not output and d['max_input_channels'] > 0:
            return i
    return None  # if not found

seeed_output = get_seeed_device(output=True)
seeed_input  = get_seeed_device(output=False)

if seeed_output is None or seeed_input is None:
    raise RuntimeError("Seeed device not found!")

# --- Test Speaker ---
duration = 3  # seconds
sample_rate = 44100  # Hz

print("Playing test tone...")
frequency = 440  # Hz (A4 note)
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
tone = 0.5 * np.sin(2 * np.pi * frequency * t)
sd.play(tone, samplerate=sample_rate, device=seeed_output)
sd.wait()

# --- Test Microphone ---
print("Recording from microphone...")
recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate,
                   channels=1, device=seeed_input)
sd.wait()
print("Recording complete.")

# --- Playback Recorded Audio ---
print("Playing back recorded audio...")
sd.play(recording, samplerate=sample_rate, device=seeed_output)
sd.wait()
print("Done.")