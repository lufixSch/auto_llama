"""Agents which can be used to extend the functionality of an LLM

Includes selectors, which decide which agent to use depending on the conversation.
"""

from ._agent import Agent, AgentResponse, AgentResponseItem
from ._selector import AgentSelector
from .selectors import SimilarityAgentSelector
from .code import CodeAgent, CodeExecAgent
from .research import (
    SearchAgent,
    DuckDuckGoSearchAgent,
    ArxivSearchAgent,
    WikipediaSearchAgent,
    ResearchAgent,
    MultiSearchAgent,
)
