from abc import ABC, abstractmethod


class Serializable(ABC):
    """Interface for classes that can be serealize to/from plain dictionaries (JSON)"""

    @abstractmethod
    def serialize(self) -> dict:
        """
        Serializes the  object into a dictionary.
        """

    @classmethod
    @abstractmethod
    def deserialize(cls, data: dict) -> "Serializable":
        """
        Deserializes the dictionary into an instance of the class.
        """
