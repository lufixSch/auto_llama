from abc import abstractmethod
from typing import Literal
from itertools import islice

from auto_llama import Agent, AgentResponse, AgentResponseItem, PromptTemplate, LLMInterface, exceptions
from auto_llama.data import Article

AGENT_NAME = "SearchAgent"

# Agent specific dependencies
try:
    import wikipedia
    from duckduckgo_search import DDGS
    from auto_llama import nlp
except ImportError:
    raise exceptions.AgentDependenciesMissing(AGENT_NAME, "research")
except exceptions.ModuleDependenciesMissing:
    raise exceptions.AgentDependenciesMissing(AGENT_NAME, "research")


class NoResultsException(Exception):
    def __init__(self, msg: Article):
        self.msg = msg
        super().__init__(self.msg.get_formatted())


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
        super().__init__(verbose)

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
        res = self.llm.completion(prompt, stopping_strings=["\n"], max_new_tokens=100)
        res = res.strip().strip('"').strip("'")

        self.print(f"Preprocessed query: {res}", verbose=True)
        return res

    def _nlp_preprocessor(self, request: str):
        """Generate search query from text input using NLP preprocessing"""

        res = nlp.to_lower(request)
        res = nlp.merge_spaces(res)
        res = nlp.remove_specific_pos(res)
        res = nlp.lemmatize(res)

        self.print(f"Preprocessed query: {res}", verbose=True)

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

        try:
            res = self._search(query)

            # Save results, if memory interface is provided
            if self.memory:
                self.memory.save(res.values())
        except exceptions.AgentUnavailableError:
            self.print("No good Search Result was found", verbose=True)

            # TODO make this prompt configurable, consider changing this to CHAT or RESPONSE to force 'I don't know!' answers.
            res = AgentResponse(
                AgentResponseItem(
                    AgentResponseItem.POSITION.CONTEXT,
                    Article(text="Unable to find results regarding this topic", src="web-search"),
                )
            )
        except NoResultsException as e:
            res = AgentResponse(
                AgentResponseItem(
                    AgentResponseItem.POSITION.CONTEXT,
                    e.msg,
                )
            )

        return res


class WikipediaSearchAgent(SearchAgent):
    """Search Wikipedia for Information"""

    def _search(self, query: str) -> AgentResponse:
        articles = wikipedia.search(query)[: self.max_results]

        responses = AgentResponse.empty()
        for article in articles:
            try:
                summary = wikipedia.summary(article, auto_suggest=False)
            except wikipedia.PageError:
                continue

            responses.append(
                AgentResponseItem(
                    AgentResponseItem.POSITION.CONTEXT, Article(text=summary, title=article, src="wikipedia")
                )
            )

        if len(responses.values()) <= 0:
            self.print("No good Search Result was found", verbose=True)

            # TODO make this prompt configurable, consider changing this to CHAT or RESPONSE to force 'I don't know!' answers.
            raise NoResultsException(Article(text="Unable to find results regarding this topic", src="wikipedia"))

        return responses


class DuckDuckGoSearchAgent(SearchAgent):
    """Search DuckDuckGo for Information"""

    def _search(self, query: str) -> AgentResponse:
        with DDGS() as ddgs:
            responses = AgentResponse.empty()
            for t in islice(ddgs.text(query), self.max_results):
                responses.append(
                    AgentResponseItem(
                        AgentResponseItem.POSITION.CONTEXT, Article(text=t["body"], title=t["title"], src=t["href"])
                    )
                )

            if len(responses.values()) <= 0:
                self.print("No good Search Result was found", verbose=True)

                # TODO make this prompt configurable, consider changing this to CHAT or RESPONSE to force 'I don't know!' answers.
                raise NoResultsException(Article(text="Unable to find results regarding this topic", src="duckduckgo"))

            return responses
