""" Different solutions for deciding which agent to use """

from ._general import CommandAgentSelector, KeywordAgentSelector
from ._txtai import SimilarityAgentSelector
from ._llm import LLMAgentSelector, AgentOverviewTemplate, AgentSelectionTemplate
