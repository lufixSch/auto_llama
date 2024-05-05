from typing import Any

from auto_llama_api.lib import Agent, Agents
from auto_llama_api.models import AgentInfo, AgentResponses, AgentsInfo
from fastapi import APIRouter, HTTPException

agentRouter = APIRouter(prefix="/agent", tags=["AutoLLaMa"])


@agentRouter.get("/", response_model=AgentsInfo)
async def list_agents(agents: Agents):
    return AgentsInfo(
        agents={
            name: AgentInfo(name=name, description=agent.description, parameters=agent.parameters)
            for name, agent in agents.items()
        }
    )


@agentRouter.post("/{agent_name}", response_model=AgentResponses)
async def run_agent(agent: Agent, params: dict[str, Any]):
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found!")

    res = agent.run(**params)
    return AgentResponses.from_agent_response_items(res.items())
