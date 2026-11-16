"""Synthesize wake word samples with Piper TTS (Polish and English voices)."""

import wave
from pathlib import Path

from piper import PiperVoice, SynthesisConfig

# wakeword/training/data, outside git (see .gitignore)
DATA_DIR   = Path(__file__).resolve().parents[1] / "data"
VOICES_DIR = DATA_DIR / "voices"

# Polish voices read the text; English ones get phonemes,
# because English espeak reads "Okapi" as AH-kap-ee
PHRASE_PL = "Hej Okapi"
PHRASE_EN = "[[ hˈeɪ oʊkˈɑːpi ]]"


def phrase_for(voice: PiperVoice) -> str:
    """Pick the wake phrase in the voice's language.

    :param voice: loaded Piper voice
    :return:      Polish text or raw English phonemes
    """
    return PHRASE_PL if voice.config.espeak_voice == "pl" else PHRASE_EN


def record_voice(voice: PiperVoice, text: str, speaker: int, path: Path):
    """Synthesize one clip and save it as WAV in the voice's sample rate.

    :param voice:   loaded Piper voice
    :param text:    text, or raw phonemes in [[ ]]
    :param speaker: speaker id, ignored by single-speaker voices
    :param path:    output WAV file
    """
    with wave.open(str(path), "wb") as wav:
        voice.synthesize_wav(text, wav, SynthesisConfig(speaker_id=speaker))


def loop_speakers(voice: PiperVoice, name: str, out_dir: Path):
    """Synthesize the wake phrase with the first few speakers of one voice.

    :param voice:   loaded Piper voice
    :param name:    voice name, used as the file name prefix
    :param out_dir: folder for the WAV files
    """
    for speaker in range(min(voice.config.num_speakers, 5)):   # multi-speaker: first 5
        record_voice(voice, phrase_for(voice), speaker, out_dir / f"{name}_{speaker}.wav")


def main():
    """Synthesize the wake phrase with every downloaded voice (first listening test)."""
    out_dir = DATA_DIR / "tts" / "probe"
    out_dir.mkdir(parents=True, exist_ok=True)
    for model in sorted(VOICES_DIR.glob("*.onnx")):
        voice = PiperVoice.load(model)
        loop_speakers(voice, model.stem, out_dir)
        print(f"{model.stem}: {voice.config.num_speakers} speaker(s), {voice.config.sample_rate} Hz")


if __name__ == "__main__":
    main()
