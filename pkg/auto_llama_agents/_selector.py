from abc import ABC, abstractmethod
from typing import TypeVar

from auto_llama import Chat

from ._agent import AgentInfo, AgentResponse

T = TypeVar("T")


class AgentSelector(ABC):
    """Base class for deciding which agents tor run based on an input"""

    @abstractmethod
    def run(self, chat: Chat, available_agents: dict[str, AgentInfo]) -> AgentResponse:
        """Select and run agents based on the conversation"""

    def _filter_agents(self, available_agents: list[str], agents: dict[str, T]) -> dict[str, T]:
        return {name: agents[name] for name in available_agents}
