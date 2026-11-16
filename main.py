from voice.mic          import Mic
from voice.wake         import WakeWord
from config.constants   import RATE, WAKE_BLOCK_SAMPLES
from config.settings    import settings


def main():
    wake  = WakeWord(name=settings.wake_word, threshold=settings.wake_threshold)
    mic   = Mic( rate=RATE, device=settings.mic_device )

    # main loop: read the microphone until stopped with Ctrl+C
    while True:
        samples = mic.read(WAKE_BLOCK_SAMPLES)
        if wake.detected(samples):
            print(">>> wake word detected")


if __name__ == "__main__":
    main()
