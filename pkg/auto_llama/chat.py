from typing import Literal, TypeAlias

ChatRoles: TypeAlias = Literal["system", "user", "assistant"]


class ChatMessage:
    """Chat message"""

    def __init__(self, role: ChatRoles, message: str):
        self.role = role
        self.message = message


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

    def append(self, role: ChatRoles, message: str) -> "Chat":
        """Add message to the chat history"""

        self._history.append(ChatMessage(role, message))
