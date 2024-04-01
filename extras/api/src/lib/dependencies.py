from typing import Annotated
from fastapi import Depends
from auto_llama.llm import LocalOpenAILLM
from auto_llama import LLMInterface as AutoLLaMaLLM

local_llm = LocalOpenAILLM(base_url="http://127.0.0.1:5001/v1")


def get_llm():
    return local_llm


LLMInterface = Annotated[AutoLLaMaLLM, Depends(get_llm)]
