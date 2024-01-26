from abc import ABC, abstractmethod

from numpy.typing import NDArray


class TTSInterface(ABC):
    """Base class for Text to speech tools"""

    @abstractmethod
    def convert(self, text: str) -> tuple[NDArray, int]:
        """Convert text to speach

        Returns:
          speech (np.NDArray): Speach signal as array
          fs (int): Sampling frequency
        """


class STTInterface(ABC):
    """Base class for Speach to text tools"""

    @abstractmethod
    def convert(self, audio: NDArray, fs: int) -> str:
        """Convert speech audio to text"""
