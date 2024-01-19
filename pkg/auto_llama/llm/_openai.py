from typing import Generator

from auto_llama import LLMInterface, Chat, exceptions

HAS_DEPENDENCIES = True

try:
    from openai import OpenAI as OpenAIClient
except ImportError:
    HAS_DEPENDENCIES = False


class LocalOpenAILLM(LLMInterface):
    """Implementation of the LLM Interface for local LLMs using OpenAI API"""

    def __init__(
        self,
        base_url: str = None,
        stopping_strings: list[str] = None,
        temperature: float = None,
        max_new_tokens: int = 200,
    ) -> None:
        if not HAS_DEPENDENCIES:
            raise exceptions.LLMDependenciesMissing(self.__class__.__name__, "openai")

        self.config = {}
        if stopping_strings:
            self.config["stop"] = stopping_strings
        if temperature:
            self.config["temperature"] = temperature
        if max_new_tokens:
            self.config["max_tokens"] = max_new_tokens

        self.client = OpenAIClient(base_url=base_url, api_key="NONE")

    def completion(self, prompt: str, stopping_strings: list[str] = [], max_new_tokens: int = None) -> str:
        self.config["stop"] = [*stopping_strings, *self.config.get("stop", [])]
        self.config["max_tokens"] = max_new_tokens or self.config.get("max_tokens", 200)

        res = self.client.completions.create(prompt=prompt, model="NONE", **self.config)
        return res.choices[0].text

    def completion_stream(
        self, prompt: str, stopping_strings: list[str] = ..., max_new_tokens: int = None
    ) -> Generator[str, None, None]:
        self.config["stop"] = [*stopping_strings, *self.config.get("stop", [])]
        self.config["max_tokens"] = max_new_tokens or self.config.get("max_tokens", 200)

        res = self.client.completions.create(prompt=prompt, model="NONE", stream=True, **self.config)

        try:
            for chunk in res:
                yield chunk.choices[0].text or ""
        finally:
            res.response.close()

    def chat(self, chat: Chat) -> Chat:
        opain_chat_history = [{"role": chat_msg.role, "content": chat_msg.message} for chat_msg in chat.history]
        res = self.client.chat.completions.create(messages=opain_chat_history, model="NONE", **self.config)

        chat.append("assistant", res.choices[0].message.content)
        return chat
