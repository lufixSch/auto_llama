from abc import ABC, abstractmethod
from enum import Enum
from typing import Any

from ._chat import Chat
from ._memory import Memory


class AgentResponse:
    """A response object from the agent"""

    class RESPONSE_TYPE(Enum):
        """Different types of answers from the AutoLLaMa Agent"""

        CONTEXT = "context"
        """ Text based result which should be added to the context """

        IMG = "img"
        """ Result Image which should be added to the response """

        CHAT = "chat"
        """ Text based result which should be added to the user input """

        PROMPT = "prompt"
        """ Text based result which replaces the current prompt in the chat"""

        RESPONSE = "response"
        """ Text based result which should be added to the response """

    def __init__(self, responses: list[tuple[RESPONSE_TYPE, str]] | tuple[RESPONSE_TYPE, str]):
        if isinstance(responses, tuple):
            responses = [responses]

        self._responses = responses

    @classmethod
    def with_same_type(cls, type: RESPONSE_TYPE, responses: list[str]):
        """Initializes AgetnResponse with the same type for all the responses"""

    def items(self):
        """List of agent responses and the response type"""

        return self._responses

    def values(self):
        """List of agent responses (Without the response type)"""

        return [response[1] for response in self._responses]

    def filter(self, filter: RESPONSE_TYPE) -> list[tuple[RESPONSE_TYPE, str]]:
        """Filters the responses by the response type"""

        return [r for r in self._responses if r[0] == filter]

class AgentInputPreprocessor(ABC):
    """
    Preprocessor for Agent text inputs which are executed before running the agent
    """

    @abstractmethod
    def __call__(self, input: str) -> str:
        """Run preprocessor with inpput text"""


class AgentChatPreprocessor(ABC):
    """
    Preprocessor for Agent chat inputs which generates a text input from the given history
    """

    @abstractmethod
    def __call__(self, chat: Chat) -> str:
        """Run preprocessor with input chat"""


class Agent(ABC):
    """Agent baseclass"""

    memory: Memory = None
    _preprocessor: AgentInputPreprocessor = None
    _chat_preprocessor: AgentChatPreprocessor = None

    def __init__(self, verbose=False, *args, **kwargs) -> None:
        self._verbose = verbose

    @abstractmethod
    def _run(self, input: str) -> AgentResponse:
        """Run agent with an input text

        This must be implemented by the inheriting agent class.
        """

    def run(self, input: str) -> AgentResponse:
        """Run agent with an input text"""

        self.print("Running ...", seperator="=")

        if self._preprocessor:
            input = self._preprocessor(input)

        self.print(f"Prompt: {input}", verbose=True)

        return self._run(input)

    def _chat(self, chat: Chat) -> AgentResponse:
        """Run agent with chat history (conversation)

        Generates prompt using given preprocessor (default: last message) and exectues `_run()` with this input

        Can be implemented by an inheriting Agent if more frredom in handling chats is needed
        """

        if self._chat_preprocessor:
            prompt = self._preprocessor(chat)
        else:
            prompt = chat.history[-1].message

        self.print(f"Prompt: {prompt}", verbose=True)

        return self._run(prompt)

    def chat(self, chat: Chat) -> AgentResponse:
        """Run agent with chat history (conversation)"""

        self.print("Running ...", seperator="=")
        self._chat(chat)

    def print(
        self,
        msg: str,
        seperator: str = None,
        verbose: bool = False,
        verbose_alt: str = None,
    ):
        """Print a formatted  message to the console

        Arguments:
            msg (str): Message, which will be printed
            separator (str): Symbol based on which a separator will be printed before the message
            verbose (bool): Wether this is a verbose message. If True, this message will only be printed if the agent is in verbose mode
            verbose_alt (str): An alternative message to be printed if the agent is in verbose mode
        """

        if self._verbose:
            if not verbose:
                return

            if verbose_alt:
                msg = verbose_alt

        if seperator:
            print(f"{seperator * 30}")

        name = self.__class__.__name__
        print(f"{name}: {msg}")

    def set_memory(self, memory: Memory):
        """Set long term memory for the agent"""

        self.memory = memory
        return self

    def set_preprocessor(self, input: AgentInputPreprocessor = None, chat: AgentChatPreprocessor = None):
        """Set preprocessor for regular text and chat inputs"""

        self._preprocessor = input or self._preprocessor
        self._chat_preprocessor = chat or self._chat_preprocessor

        return self
