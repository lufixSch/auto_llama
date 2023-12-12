from abc import ABC, abstractmethod

from ._chat import Chat


class LLMInterface(ABC):
    """Generic  LLM Interface"""

    @abstractmethod
    def completion(self, prompt: str, stopping_strings: list[str] = [], max_new_tokens: int = None) -> str:
        """Run LLM completion on a given prompt

        stopping_strings will extend the default stopping strings,
        max_new_tokens will overwrite  the default configuration
        """

    def chat(self, chat: Chat, stopping_strings: list[str] = [], max_new_tokens: int = None) -> Chat:
        """Generate next message in a chat"""

        prompt = chat.prompt
        res = self.completion(prompt, stopping_strings, max_new_tokens)
        chat.append("assistant", res)

        return chat
