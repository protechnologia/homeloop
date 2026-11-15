from voice.mic        import Mic
from voice.sound      import Sound
from config.constants import RATE, WAKE_BLOCK_SAMPLES
from config.settings  import settings


def main():
    mic = Mic( rate=RATE, device=settings.mic_device )
    while True:
        sound = Sound(mic.read(WAKE_BLOCK_SAMPLES))  # 80 ms of audio
        print("#" * int(sound.loudness / 100))       # loudness bar in the terminal


if __name__ == "__main__":
    main()
