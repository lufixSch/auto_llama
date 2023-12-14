from abc import ABC, abstractmethod

from ._agent import AgentResponse
from ._chat import Chat

class InputPreprocessor(ABC):
    """
    Preprocessor for Agent text inputs which are executed before running the agent
    """

    @abstractmethod
    def __call__(self, input: str) -> str:
        """Run preprocessor with inpput text"""


class ChatPreprocessor(ABC):
    """
    Preprocessor for Agent chat inputs which generates a text input from the given history
    """

    @abstractmethod
    def __call__(self, chat: Chat) -> str:
        """Run preprocessor with input chat"""


class AgentManager(ABC):
    """Base class for managing/executing agents based on an input"""

    _preprocessor: InputPreprocessor = None
    _chat_preprocessor: ChatPreprocessor = None

    @abstractmethod
    def _run(self, prompt: str) -> AgentResponse:
        """Run agents based on text input"""

    def run_agents(self, input: str | Chat) -> AgentResponse:
        """Run agents based on text input or chat history"""

        if isinstance(input, str):
            if self._preprocessor:
                input = self._preprocessor(input)

            return self._run(input)
        else:
            if self._chat_preprocessor:
                prompt = self._preprocessor(input)
            else:
                prompt = input.history[-1].message

            return self._run_chat(prompt)

    def set_preprocessor(self, input: InputPreprocessor = None, chat: ChatPreprocessor = None):
        """Set preprocessor for regular text and chat inputs"""

        self._preprocessor = input or self._preprocessor
        self._chat_preprocessor = chat or self._chat_preprocessor

        return self