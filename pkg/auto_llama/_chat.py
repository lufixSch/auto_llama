from typing import Literal, TypeAlias, Callable
from datetime import datetime
from uuid import uuid4

ChatRoles: TypeAlias = Literal["system", "user", "assistant"]


class ChatMessage:
    """Chat message"""

    def __init__(self, role: ChatRoles, message: str, date: datetime = None):
        self.role = role
        self.message = message
        self.date = date or datetime.now()

    def to_string(self, name: str = None):
        return f"{self.date.isoformat()} - {name or self.role}: {self.message}"


class Chat:
    """Chat history"""

    _history: list[ChatMessage]
    _names: dict[ChatRoles, str]
    _listeners: dict[str, Callable[[ChatMessage, "Chat"], None]]

    def __init__(
        self,
        system_message: str = None,
        names: dict[ChatRoles, str] = {"system": "system", "user": "user", "assistant": "assistant"},
    ):
        """
        Args:
            system_message (str): Initial system message (First message in the chat). Defaults to None.
            names (dict[ChatRoles, str]): Mapping from generic chat roles to displayed names.
        """

        self._history = []
        self._listeners = {}
        self._names = names
        self._has_system_message = bool(system_message)
        self.append("system", system_message)
        self._system_template = system_message

    @classmethod
    def from_history(
        cls,
        history: list[ChatMessage],
        system_message: str = None,
        names: dict[ChatRoles, str] = {"system": "system", "user": "user", "assistant": "assistant"},
    ):
        """Initialize a new chat from a chat history"""

        chat = cls(system_message, names)
        chat._history = [*chat.history, *history]
        return chat

    @property
    def prompt(self) -> str:
        """Formatted chat prompt

        NOTE: Instruction patterns are not supported yet!
        """

        return "\n".join([chat_msg.to_string(self._names[chat_msg.role]) for chat_msg in self.history])

    @property
    def history(self) -> list[ChatMessage]:
        """chat history"""

        return self._history

    @property
    def last(self) -> ChatMessage:
        """last chat message"""

        return self.history[-1]

    @property
    def names(self) -> dict[ChatRoles, str]:
        """Mapping from generic chat roles to displayed names"""

        return self._names

    @property
    def len(self) -> int:
        """Length of chat history

        Ignores the system message
        """

        cnt = len(self._history)
        cnt -= 1 if self._has_system_message else 0

        return cnt

    def name(self, role: ChatRoles):
        """Return name base on role"""

        return self._names[role]

    def append(self, role: ChatRoles, message: str, date: datetime = None):
        """Add message to the chat history"""

        chat_message = ChatMessage(role, message, date)
        self._history.append(chat_message)

        for listener in self._listeners.values():
            listener(chat_message, self)

        return chat_message

    def filter(
        self,
        include_roles: list[ChatRoles] = ["user", "assistant", "system"],
        exclude_roles: list[ChatRoles] = [],
        filter_cb: Callable[[ChatMessage], bool] = lambda _: True,
    ) -> list[ChatMessage]:
        """Filter chat history based on roles

        Args:
            include_roles (list[ChatRoles]): List of roles to include
            exclude_roles (list[ChatRoles]): List of roles not to include
            filter_cb (Callable[[ChatMessage], bool]): Custom filter function. Will be called for each message.
            The message wil be included if the function returns `True`
        """

        return [
            chat_msg
            for chat_msg in self.history
            if (chat_msg.role in include_roles) and (chat_msg.role not in exclude_roles) and filter_cb(chat_msg)
        ]

    def format_system_message(self, context: str, old_chat: dict[str, ChatMessage]):
        """Format system message and overwrite current system message (e.g. chat.history[0])"""

        if not self._has_system_message:
            return ""

        system_message = self._system_template.format(
            assistant=self.name("assistant"),
            name=self.name("user"),
            context=context,
            old_chat="\n".join([chat.to_string(name) for name, chat in old_chat.items()]),
        )

        if self._history[0].role != "system":
            raise ValueError("Could not find system message")

        self._history[0] = ChatMessage("system", system_message)

        return system_message

    def last_from(self, role: ChatRoles) -> str:
        """Return last chat message of a given role"""

        for chat_msg in reversed(self.history):
            if chat_msg.role == role:
                return chat_msg.message

        raise ValueError(f"No message found for role '{role}'")

    def clone(self, start: int = 0, end: int = None) -> "Chat":
        """Clone chat from start to end

        WARNING: No deep copy of ChatMessages
        """

        new_chat = Chat(self._names)

        if end:
            new_chat._history = self._history[start:end]
        else:
            new_chat._history = self._history[start:]

        return new_chat

    def trunc(self, max_len: int) -> list[ChatMessage]:
        """Truncate chat history to maximum length

        Ignores the system message

        Returns:
            deleted (list[ChaMessage]): Deleted chat messages
        """

        if self.len <= max_len:
            return []

        start = 1 if self._has_system_message else 0
        return [self._history.pop(start) for _ in range(start, start + (self.len - max_len))]

    def new_message_listener(self, listener: Callable[[ChatMessage, "Chat"], None]) -> str:
        """Register a callback which will be called every time a new message is added to the chat

        Returns:
            id (str): listener id necessary for removing the listener
        """

        id = uuid4().hex
        self._listeners[id] = listener

        return id

    def remove_new_message_listener(self, id: str):
        """Remove listener by id"""

        self._listeners.pop(id)
