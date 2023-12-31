from abc import ABC, abstractmethod
from enum import Enum

from ._memory import Memory
from .data import Content, Article, Image, ImageSource


class AgentResponseItem:
    """Single Item in an agent response"""

    type: "TYPE"

    class TYPE(Enum):
        """Different  types of responses"""

        TEXT = "text"
        """  Text response """

        IMG_SRC = "image_src"
        """External Image response as source path/url """

        IMG = "image"
        """ Image response with image object """

    class POSITION(Enum):
        """Where to inject the response"""

        CONTEXT = "context"
        """Add the response to the context"""

        RESPONSE = "response"
        """ Add the response to the response"""

        CHAT = "chat"
        """ Add the response to the user chat message"""

    def __init__(self, position: POSITION, value: Content | str) -> None:
        self.position = position
        self._value = value

        if isinstance(value, str):
            value = Article(value)
            self.type = self.TYPE.TEXT
        elif isinstance(value, Article):
            self.type = self.TYPE.TEXT
        elif isinstance(value, Image):
            self.type = self.TYPE.IMG
        elif isinstance(value, ImageSource):
            self.type = self.TYPE.IMG_SRC

    @property
    def value(self) -> Content:
        """Get the value of the response"""
        return self._value

    @property
    def collection(self) -> tuple[POSITION, TYPE, Content]:
        """Tuple of the position, type and value of the response"""
        return self.position, self.type, self._value

    def to_string(self) -> str:
        """Return the response as a string (markdown)"""
        return self._value.get_formatted()

    def collection_str(self) -> tuple[POSITION, TYPE, str]:
        """Tuple of the position, type and value of the response as string"""

        return self.position, self.type, self.to_string()


class AgentResponse:
    """A response object from the agent"""

    def __init__(self, responses: list[AgentResponseItem] | AgentResponseItem):
        if isinstance(responses, AgentResponseItem):
            responses = [responses]

        self._responses = responses

    @classmethod
    def empty(cls):
        """Initializes empty Response"""

        return cls([])

    @classmethod
    def with_same_pos(
        cls,
        pos: AgentResponseItem.POSITION,
        responses: list[Content | str],
    ):
        """Initializes AgentResponse with the same type and position for all the responses"""

        return cls([AgentResponseItem(pos, res) for res in responses])

    def append(self, responses: list[AgentResponseItem] | AgentResponseItem):
        """Appends responses to the current list off responses"""

        if isinstance(responses, AgentResponseItem):
            responses = [responses]

        self._responses.extend(responses)

    def items(self):
        """List of agent responses and the response type"""

        return self._responses

    def values(self) -> list[Content]:
        """List of agent response values"""

        return [response.value for response in self._responses]

    def filter(self, filter: AgentResponseItem.TYPE) -> list[AgentResponseItem]:
        """Filters the responses by the response type"""

        return [r for r in self._responses if r.type == filter]


class Agent(ABC):
    """Agent baseclass"""

    memory: Memory = None

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
        self.print(f"Prompt: {input}", verbose=True)

        return self._run(input)

    def print(
        self,
        msg: str,
        seperator: str = None,
        verbose: bool = False,
        verbose_alt: str = None,
    ):
        """Print a formatted  message to the console

        Args:
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
