from typing import Any

from auto_llama_agents import AgentResponseItem

from .base import BaseSchema


class AgentInfo(BaseSchema):
    """Information about one agent (pydantic equivalent to `auto_llama_agents.AgentInfo`)"""

    name: str
    description: str
    parameters: dict[str, str]


class AgentsInfo(BaseSchema):
    """Information about the available agents"""

    agents: dict[str, AgentInfo]


class AgentResponse(BaseSchema):
    """Representation of an agent response"""

    type: AgentResponseItem.TYPE
    position: AgentResponseItem.POSITION
    value: dict[str, Any]

    @classmethod
    def from_response_item(cls, item: AgentResponseItem):
        """Initialize from `auto_llama_agents.AgentResponseItem`"""

        return cls(type=item.type, position=item.position, value=item.value.serialize())


class AgentResponses(BaseSchema):
    """A group of agent responses"""

    items: list[AgentResponse]

    @classmethod
    def from_agent_response_items(cls, items: list[AgentResponseItem]):
        """Initialize from `auto_llama_agents.AgentResponseItem`"""

        return cls(items=[AgentResponse.from_response_item(item) for item in items])
