from auto_llama import TTS, STT, exceptions
from numpy.typing import NDArray

try:
    from txtai.pipeline import Transcription, TextToSpeech

    _transcribe = Transcription(path="distil-whisper/distil-large-v2")
    _tts = TextToSpeech()
except ImportError:
    raise exceptions.DependenciesMissing("speech", "speech", "txtai")


class TxtAITTS(TTS):
    def convert(self, text: str) -> tuple[NDArray, int]:
        return _tts(text)


class TxtAISTT(STT):
    def convert(self, audio: NDArray, fs: int) -> str:
        return _transcribe(audio, rate=fs)
