from abc import ABC, abstractmethod

from auto_llama import Chat
from ._agent import AgentResponse


class AgentSelector(ABC):
    """Base class for deciding which agents tor run based on an input"""

    @abstractmethod
    def run(self, chat: Chat) -> AgentResponse:
        """Select and run agents based on the conversation"""
