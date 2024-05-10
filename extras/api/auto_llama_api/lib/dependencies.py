from typing import Annotated, Callable

from auto_llama_agents import Agent as AutoLLamaAgent
from auto_llama_api import auto_llama_config
from auto_llama_memory import Memory
from fastapi import Depends, UploadFile

from auto_llama import LLMInterface as AutoLLaMaLLM
from auto_llama.text import FileLike, FileLoader

_active_memory = auto_llama_config.default_memory


def get_llm():
    return auto_llama_config.llm


LLMInterface = Annotated[AutoLLaMaLLM, Depends(get_llm)]


def get_memories():
    return auto_llama_config.memory


Memories = Annotated[dict[str, Memory], Depends(get_memories)]


def get_active_memory():
    return auto_llama_config.memory.get(_active_memory, None)


ActiveMemory = Annotated[Memory, Depends(get_active_memory)]


def get_active_memory_setter():
    def setter(name: str | None):
        global _active_memory
        _active_memory = name

    return setter


ActiveMemorySetter = Annotated[Callable[[str | None], None], Depends(get_active_memory_setter)]


def get_agents():
    return auto_llama_config.agents


Agents = Annotated[dict[str, AutoLLamaAgent], Depends(get_agents)]


def get_agent(agent_name: str):
    return auto_llama_config.agents.get(agent_name, None)


Agent = Annotated[AutoLLamaAgent, Depends(get_agent)]


def get_file_loaders():
    return auto_llama_config.file_loaders


FileLoaders = Annotated[list[FileLoader], Depends(get_file_loaders)]


def get_file_like(file: UploadFile):
    return FileLike(file.filename, file.file)


UploadedFile = Annotated[FileLike, Depends(get_file_like)]
