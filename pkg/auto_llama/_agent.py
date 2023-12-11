from abc import ABC, abstractmethod
from enum import Enum

from ._chat import Chat


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

    def get(self):
        """List of agent responses and the response type"""

        self._responses

    def filter(self, filter: RESPONSE_TYPE) -> list[tuple[RESPONSE_TYPE, str]]:
        """Filters the responses by the response type"""

        return [r for r in self._responses if r[0] == filter]


class Agent(ABC):
    """Agent baseclass"""

    def __init__(self, verbose=False, *args, **kwargs) -> None:
        self._verbose = verbose

    @abstractmethod
    def _run(self, input: str) -> AgentResponse:
        """Run agent with an input text

        This must be implemented by the inheriting agent class.
        """

        raise NotImplementedError()

    def run(self, input: str) -> AgentResponse:
        """Run agent with an input text"""

        self.print("Running ...", seperator="=", verbose=True, verbose_alt=f"Running ...\nPrompt: {input}")
        self._run(input)

    @abstractmethod
    def _chat(self, chat_history: Chat) -> AgentResponse:
        """Run agent with chat history (conversation)

        This must be implemented by the inheriting agent class.
        """

        raise NotImplementedError()

    def chat(self, chat_history: Chat) -> AgentResponse:
        """Run agent with chat history (conversation)"""

        self.print(
            "Running ...", seperator="=", verbose=True, verbose_alt=f"Running ...\nPrompt: {chat_history.prompt}"
        )
        self._chat(chat_history)

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

        if verbose:
            if not self._verbose:
                return

            if verbose_alt:
                msg = verbose_alt

        if seperator:
            print("f{seperator * 10}")

        name = self.__class__.__name__
        print(f"{name}: {msg}")
