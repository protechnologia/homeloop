import numpy as np


class Sound:
    """Block of audio samples (mono, int16) and measures derived from it."""

    def __init__(self, samples: np.ndarray):
        self.samples = samples

    @property
    def loudness(self) -> float:
        # average distance from zero; int32 because abs(-32768) does not fit in int16
        return float(np.abs(self.samples.astype(np.int32)).mean())
