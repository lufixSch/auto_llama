from abc import ABC, abstractmethod
from typing import Generator

from ._chat import Chat


class LLMInterface(ABC):
    """Generic  LLM Interface"""

    @abstractmethod
    def completion(self, prompt: str, stopping_strings: list[str] = [], max_new_tokens: int = None) -> str:
        """Run LLM completion on a given prompt

        stopping_strings will extend the default stopping strings,
        max_new_tokens will overwrite  the default configuration
        """

    @abstractmethod
    def completion_stream(
        self, prompt: str, stopping_strings: list[str] = [], max_new_tokens: int = None
    ) -> Generator[str, None, None]:
        """Run LLM completion on a given prompt

        stopping_strings will extend the default stopping strings,
        max_new_tokens will overwrite  the default configuration

        Returns response as a stream of tokens
        """

    def chat(self, chat: Chat, stopping_strings: list[str] = [], max_new_tokens: int = None) -> Chat:
        """Generate next message in a chat"""

        prompt = chat.prompt
        res = self.completion(prompt, stopping_strings, max_new_tokens)
        chat.append("assistant", res)

        return chat

    def chat_stream(
        self, chat: Chat, stopping_strings: list[str] = [], max_new_tokens: int = None
    ) -> Generator[str, None, None]:
        """Generate next message in a chat

        Returns response as a stream of tokens
        """

        prompt = chat.prompt
        res = self.completion_stream(prompt, stopping_strings, max_new_tokens)
        chat.append("assistant", "")

        try:
            for chunk in res:
                chat.last.message += chunk
                yield chunk
        finally:
            res.close()

        return res
