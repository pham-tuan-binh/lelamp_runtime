import subprocess
from datetime import datetime

import pvporcupine
from pvrecorder import PvRecorder


ACCESS_KEY = "paFqGTMGoy+jOvwxt/aw+QDm4G/Ajuf6d40GCrtNXe1JFI5D4WltXQ=="
KEYWORD = "./wake_up.ppn"


def main():
    porcupine = pvporcupine.create(
        access_key=ACCESS_KEY,
        keyword_paths=[KEYWORD],
        sensitivities=[0.5]
    )

    recorder = PvRecorder(
        frame_length=porcupine.frame_length,
        device_index=-1
    )
    recorder.start()

    print(f"Listening for '{KEYWORD}'... (Ctrl+C to exit)")

    try:
        while True:
            pcm = recorder.read()
            result = porcupine.process(pcm)

            if result >= 0:
                print(f"[{datetime.now()}] Detected {KEYWORD}")
                recorder.delete()
                porcupine.delete()
                print("Running: sudo uv run main.py console")
                subprocess.run(["sudo", "uv", "run", "main.py", "console"])
                break
    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        try:
            recorder.delete()
        except:
            pass
        try:
            porcupine.delete()
        except:
            pass


if __name__ == "__main__":
    main()