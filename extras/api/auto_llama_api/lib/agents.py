from auto_llama_agents import Agent, AgentInfo
from auto_llama_api.models import OpenAITool


def resolve_agents(tools: list[OpenAITool], agents: dict[str, Agent]) -> dict[str, AgentInfo]:
    """Resolve list available agents using the given list of tools and configured agents"""

    available_agents = {}

    for tool in tools:
        if tool.type != "function":
            raise ValueError(f"Unsupported tool type: {tool.type}")

        agent = agents.get(tool.function.name, None)
        if agent is None:
            raise ValueError(f"No agent configured for tool: {tool.function.name}")

        # Use default description/parameters if none are provided
        available_agents[tool.function.name] = AgentInfo.with_agent(
            agent, tool.function.name, tool.function.description, None
        )
        # TODO integrate OpenAI parameter schema

    return available_agents
