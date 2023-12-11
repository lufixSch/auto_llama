from abc import abstractmethod
from typing import Literal

from auto_llama import Agent, AgentResponse, PromptTemplate, LLMInterface, nlp

AGENT_NAME = "SearchAgent"

# Agent specific dependencies


class SearchPromptTemplate(PromptTemplate):
    """Prompt template for generating a usefull search query from a text input.

    Parameters:
        tool (str): The tool which is used to search information
        request (str): The input from which the query should be generated
    """

    def format(self, tool: str, request: str) -> str:
        return super().format(tool=tool, request=request)


class SearchAgent(Agent):
    """Generic search agent"""

    SEARCH_TOOL = "generic search"
    query_generator: Literal["none", "llm", "nlp"] = "none"
    llm: LLMInterface = None
    prompt_template: SearchPromptTemplate = None

    def __init__(self, max_results: int = 1, verbose=False) -> None:
        self.max_results = max_results

    @classmethod
    def with_llm_query(
        cls, llm: LLMInterface, prompt_template: SearchPromptTemplate, max_results: int = 1, verbose=False
    ) -> "SearchAgent":
        """Init SearchAgent with LLM Model for generating search queries from text input"""

        instance = cls(max_results, verbose)
        instance.llm = llm
        instance.prompt_template = prompt_template
        instance.query_generator = "llm"

        return instance

    @classmethod
    def with_nlp_query(cls, max_results: int = 1, verbose=False):
        """Init SearchAgent with NLP preprocessing  for generating search queries from text input"""

        instance = cls(max_results, verbose)
        instance.query_generator = "nlp"
        return instance

    def _llm_preprocessor(self, request: str):
        """Generate search query from text input using LLM Model"""

        prompt = self.prompt_template.format(tool=self.SEARCH_TOOL, request=request)
        return self.llm.completion(prompt, stopping_strings=["\n"], max_new_tokens=100)

    def _nlp_preprocessor(self, request: str):
        """Generate search query from text input using NLP preprocessing"""

        res = nlp.to_lower(request)
        res = nlp.merge_spaces(res)
        res = nlp.remove_specific_pos(res)

        return res

    @abstractmethod
    def _search(self, query: str) -> AgentResponse:
        """Search for a given query"""

    def _run(self, input: str) -> AgentResponse:
        query = input

        if self.query_generator == "llm":
            query = self._llm_preprocessor(input)
        elif self.query_generator == "nlp":
            query = self._nlp_preprocessor(input)

        return self._search(query)
