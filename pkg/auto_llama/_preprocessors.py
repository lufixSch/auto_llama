from abc import ABC, abstractmethod

from ._chat import Chat


class PromptPreprocessor(ABC):
    """
    Preprocessor for text prompts
    """

    @abstractmethod
    def __call__(self, prompt: str) -> str:
        """Run preprocessor with inpput text"""


class ChatPreprocessor(ABC):
    """
    Preprocessor for chats
    """

    @abstractmethod
    def __call__(self, chat: Chat) -> Chat:
        """Run preprocessor with inpput chat"""


class ChatToObjectiveConverter(ABC):
    """
    Convert a chat into a objective/prompt
    """

    @abstractmethod
    def __call__(self, chat: Chat) -> str:
        """Run preprocessor with input chat"""
