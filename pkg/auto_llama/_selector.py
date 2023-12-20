from abc import ABC, abstractmethod

from ._agent import Agent


class AgentSelector(ABC):
    """Base class for deciding which agents tor run based on an input"""

    @abstractmethod
    def _run(self, prompt: str) -> Agent:
        """Run agents based on text input"""

    def run(self, prompt: str) -> Agent:
        """Run agents based on text input"""

        return self._run(prompt)
