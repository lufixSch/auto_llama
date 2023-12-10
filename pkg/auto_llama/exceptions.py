class AgentUnavailableError(Exception):
    def __init__(self, agent_name, error: str):
        super().__init__(f"{agent_name} is unavailable.\n{error}")


class AgentDependenciesMissing(Exception):
    def __init__(self, agent_name: str, optional_dep: str):
        super().__init__(
            f"{agent_name} is missing a dependency.\nMake sure to install optional dependencies for this agent: `pip install auto-llama[{optional_dep}]`"
        )
