"""Record wake word samples from the microphone (16 kHz, mono, int16 WAV)."""

import argparse
from datetime import datetime
from pathlib  import Path

from scipy.io import wavfile

from homeloop.voice.mic        import Mic
from homeloop.voice.sound      import Sound
from homeloop.config.constants import SAMPLES_PER_SECOND
from homeloop.config.settings  import settings

# wakeword/training/data, outside git (see .gitignore)
DATA_DIR      = Path(__file__).resolve().parents[1] / "data"
PAUSE_SECONDS = 1   # between clips: time to breathe, the audio is discarded
CLIP_SECONDS  = 3   # longer than the phrase: trimmed to the model window in step 5


def record_positive(mic: Mic, count: int, out_dir: Path):
    """Record wake word clips one after another, with a pause in between.

    :param mic:     microphone with a running stream
    :param count:   number of clips to record
    :param out_dir: folder for the WAV files, created if missing
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    for i in range(count):
        mic.read(SAMPLES_PER_SECOND * PAUSE_SECONDS)      # read and drop: keeps us in real time
        print(f"[{i + 1}/{count}] say the wake word...", end=" ", flush=True)
        samples = mic.read(SAMPLES_PER_SECOND * CLIP_SECONDS)
        wavfile.write(out_dir / f"{i:03d}.wav", SAMPLES_PER_SECOND, samples)
        print(f"loudness {Sound(samples).loudness:.0f}")  # low value = nothing was said


def main():
    """Parse arguments and record a new session of wake word clips."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--count", type=int, default=50, help="number of clips (default: 50)")
    args = parser.parse_args()

    mic     = Mic(rate=SAMPLES_PER_SECOND, device=settings.mic_device)
    session = datetime.now().strftime("%Y%m%d-%H%M%S")    # one folder per session (step 7)
    record_positive(mic, args.count, DATA_DIR / "positive" / session)


if __name__ == "__main__":
    main()
