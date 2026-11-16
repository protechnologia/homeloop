import numpy as np
from openwakeword.model import Model


class WakeWord:
    """Wake word detector (openWakeWord): one detection per spoken phrase."""

    def __init__( self, name: str, threshold: float ):
        """Load the openWakeWord model.

        :param name:      pre-trained model name, e.g. "hey_jarvis"
        :param threshold: detection threshold 0..1
        """
        self._name      = name
        self._threshold = threshold
        self._model     = Model( wakeword_models=[name], inference_framework="onnx" )

    def detected(self, samples: np.ndarray) -> bool:
        """Feed the next audio block to the wake word model.

        :param samples: 80 ms block of int16 samples (WAKE_BLOCK_SAMPLES)
        :return:        True once per spoken wake word
        """
        score = self._model.predict(samples)[self._name]
        if score < self._threshold:
            return False
        self._model.reset()  # clear buffers: the same phrase must not trigger again
        return True