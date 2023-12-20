from abc import ABC, abstractmethod

from ._chat import Chat


class InputPreprocessor(ABC):
    """
    Preprocessor for Agent text inputs which are executed before running the agent
    """

    @abstractmethod
    def __call__(self, input: str) -> str:
        """Run preprocessor with inpput text"""


class ChatPreprocessor(ABC):
    """
    Preprocessor for Agent chat inputs which generates a text input from the given history
    """

    @abstractmethod
    def __call__(self, chat: Chat) -> str:
        """Run preprocessor with input chat"""
