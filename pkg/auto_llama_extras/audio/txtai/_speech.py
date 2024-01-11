from auto_llama_extras.audio import TTSInterface, STTInterface
from auto_llama import exceptions, ModelLoader
from numpy.typing import NDArray

try:
    from txtai.pipeline import Transcription, TextToSpeech
except ImportError:
    raise exceptions.DependenciesMissing("speech", "speech", "txtai")

ModelLoader.add("txtai.tts", lambda: TextToSpeech())
ModelLoader.add("txtai.transcribe", lambda: Transcription(path="distil-whisper/distil-large-v2"))


class TxtAITTS(TTSInterface):
    def convert(self, text: str) -> tuple[NDArray, int]:
        return ModelLoader.get("txtai.tts", TextToSpeech)(text)


class TxtAISTT(STTInterface):
    def convert(self, audio: NDArray, fs: int) -> str:
        return ModelLoader.get("txtai.transcribe", Transcription)(audio, rate=fs)
