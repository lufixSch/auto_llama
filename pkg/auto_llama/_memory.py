from abc import ABC, abstractmethod

from ._chat import Chat, ChatMessage


class Memory(ABC):
    """Base class for Long term memory implementations"""

    @abstractmethod
    def save(self, data: str | list[str]):
        """Add new data to the memory"""

    @abstractmethod
    def remember(self, query: str, max_tokens: int = 500, max_items: int = 10) -> list[str]:
        """Find data in memory related to the query"""


class ConversationMemory(ABC):
    """ "Base class for Conversation memory implementations"""

    @abstractmethod
    def save(self, chat: Chat | list[ChatMessage]) -> None:
        """Saves a chat to memory"""

    @abstractmethod
    def remember(self, query: str, max_tokens: int = 500, max_items: int = 10) -> Chat:
        """Finds messages in memory related to the query"""
