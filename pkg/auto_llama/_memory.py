from abc import ABC, abstractmethod


class Memory(ABC):
    """Base class for Long term memory implementations"""

    @abstractmethod
    def save(self, data: str):
        """Add new data to the memory"""

    @abstractmethod
    def remember(self, query: str) -> str:
        """Find data in memory relaated to the query"""
