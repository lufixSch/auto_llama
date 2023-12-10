from abc import ABC, abstractmethod
from openai import OpenAI as OpenAIClient

from .chat import Chat


class LLMInterface(ABC):
    """Generic  LLM Interface"""

    @abstractmethod
    def completion(self, prompt: str) -> str:
        """Run LLM completion on a given prompt"""

        raise NotImplementedError()

    def chat(self, chat: Chat) -> Chat:
        """Generate next message in a chat"""

        prompt = chat.prompt
        res = self.completion(prompt)
        chat.append("assistant", res)

        return chat


class LLMLocalOpenAI(LLMInterface):
    """Implementation of the LLM Interface for local LLMs using OpenAI API"""

    def __init__(
        self,
        base_url: str = None,
        stopping_strings: list[str] = None,
        temperature: float = None,
        max_new_tokens: int = 200,
    ) -> None:
        self.config = {}
        if stopping_strings:
            self.config["stop"] = stopping_strings
        if temperature:
            self.config["temperature"] = temperature
        if max_new_tokens:
            self.config["max_tokens"] = max_new_tokens

        self.client = OpenAIClient(base_url=base_url, api_key="NONE")

    def completion(self, prompt: str) -> str:
        res = self.client.completions.create(prompt=prompt, model="NONE", **self.config)
        return res.choices[0].text

    def chat(self, chat: Chat) -> Chat:
        opain_chat_history = [{"role": chat_msg.role, "content": chat_msg.message} for chat_msg in chat.history]
        res = self.client.chat.completions.create(messages=opain_chat_history, model="NONE", **self.config)

        chat.append("assistant", res.choices[0].message.content)
        return chat
