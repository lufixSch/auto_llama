from typing import Literal, TypeAlias, Callable
from datetime import datetime

ChatRoles: TypeAlias = Literal["system", "user", "assistant"]


class ChatMessage:
    """Chat message"""

    def __init__(self, role: ChatRoles, message: str, date: datetime = None):
        self.role = role
        self.message = message
        self.date = date or datetime.now()


class Chat:
    """Chat history"""

    _history: list[ChatMessage] = []
    _names: dict[ChatRoles, str]

    def __init__(self, names: dict[ChatRoles, str] = {"system": "system", "user": "user", "assistant": "assistant"}):
        self._names = names

    @property
    def prompt(self) -> str:
        """Formatted chat prompt

        NOTE: Instruction patterns are not supported yet!
        """

        return "\n".join([f"{self._names[chat_msg.role]}: {chat_msg.message}" for chat_msg in self.history])

    @property
    def history(self) -> list[ChatMessage]:
        """chat history"""

        return self._history

    def name(self, role: str):
        """Return name base on role"""

        return self._names[role]

    def append(self, role: ChatRoles, message: str, date: datetime = None) -> "Chat":
        """Add message to the chat history"""

        self._history.append(ChatMessage(role, message, date))

    def filter(
        self,
        include_roles: list[ChatRoles] = ["user", "assistant", "system"],
        exclude_roles: list[ChatRoles] = [],
        filter_cb: Callable[[ChatMessage], bool] = lambda _: True,
    ) -> list[ChatMessage]:
        """Filter chat history based on roles

        Arguments:
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
