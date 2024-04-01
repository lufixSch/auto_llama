from typing import Annotated
from fastapi import Depends
from auto_llama import LLMInterface as AutoLLaMaLLM
from auto_llama_api import auto_llama_config


def get_llm():
    return auto_llama_config.llm


LLMInterface = Annotated[AutoLLaMaLLM, Depends(get_llm)]
