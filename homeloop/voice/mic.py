import numpy as np
import sounddevice as sd

from homeloop.config.constants import CHANNELS, DTYPE


class Mic:
    """Microphone: returns blocks of samples (mono, int16)."""

    def __init__(self, rate: int, device: str | None = None):
        # device: name + audio API (e.g. "Realtek MME"), or None for the system default
        self._stream = sd.InputStream(samplerate=rate, channels=CHANNELS, dtype=DTYPE, device=device)
        self._stream.start()

    def read(self, samples: int) -> np.ndarray:
        # wait until the requested number of samples is recorded
        block, _ = self._stream.read(samples)
        return block.flatten()
