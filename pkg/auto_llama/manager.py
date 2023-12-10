from abc import ABC, abstractmethod

from .agent import AgentResponse
from .chat import Chat


class AgentManager(ABC):
    """Base class for managing/executing agents based on an input"""

    @abstractmethod
    def _run(self, input: str) -> AgentResponse:
        """Run agents based on text input"""

        raise NotImplementedError()

    @abstractmethod
    def _run_chat(self, chat: Chat) -> AgentResponse:
        """Run agents based on chat history"""

    def run_agents(self, input: str | Chat) -> AgentResponse:
        """Run agents based on text input or chat history"""

        if isinstance(input, str):
            return self._run(input)
        else:
            return self._run_chat(input)
