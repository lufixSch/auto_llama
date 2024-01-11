from auto_llama_extras.audio import TTSInterface, STTInterface
from auto_llama import exceptions
from numpy.typing import NDArray

try:
    from txtai.pipeline import Transcription, TextToSpeech

    _transcribe = Transcription(path="distil-whisper/distil-large-v2")
    _tts = TextToSpeech()
except ImportError:
    raise exceptions.DependenciesMissing("speech", "speech", "txtai")


class TxtAITTS(TTSInterface):
    def convert(self, text: str) -> tuple[NDArray, int]:
        return _tts(text)


class TxtAISTT(STTInterface):
    def convert(self, audio: NDArray, fs: int) -> str:
        return _transcribe(audio, rate=fs)
