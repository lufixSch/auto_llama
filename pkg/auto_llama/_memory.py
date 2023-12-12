from abc import ABC, abstractmethod

from ._chat import Chat


class Memory(ABC):
    """Base class for Long term memory implementations"""

    @abstractmethod
    def save(self, data: str):
        """Add new data to the memory"""

    def save_conversation(self, chat: Chat):
        """Adds a conversation to the memory

        Passthrough to `save` with `chat.prompt` by default.
        """

        self.save(chat.prompt)

    @abstractmethod
    def remember(self, query: str, max_tokens: int = 500, max_items: int = 10) -> str:
        """Find data in memory relaated to the query"""
