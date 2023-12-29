from abc import ABC, abstractmethod

from ._chat import Chat, ChatMessage
from .data import Content


class Memory(ABC):
    """Base class for Long term memory implementations"""

    @abstractmethod
    def save(self, data: Content | list[Content]):
        """Add new data to the memory"""

    @abstractmethod
    def remember(self, query: str, max_tokens: int = 500, max_items: int = 10) -> list[Content]:
        """Find data in memory related to the query"""


class ConversationMemory(ABC):
    """ "Base class for Conversation memory implementations"""

    @abstractmethod
    def save(self, chat: Chat) -> None:
        """Saves a chat to memory"""

    @abstractmethod
    def remember(self, query: str, max_tokens: int = 500, max_items: int = 10) -> dict[str, ChatMessage]:
        """Finds messages in memory related to the query

        Returns:
            old_messages (dict[str, ChatMessage]): A dictionary of messages found in memory and the name of the person who send them
        """
