import json
import os
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

    def save(self, path: str) -> None:
        """
        Saves the object to a file.
        """

        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, "x") as f:
            json.dump(self.serialize(), f)

    @classmethod
    def load(cls, path: str) -> "Serializable":
        """
        Loads the object from a file.
        """

        with open(path, "r") as f:
            return cls.deserialize(json.load(f))
