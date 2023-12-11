"""Custom exceptions for AutoLLaMa"""

class AgentUnavailableError(Exception):
    def __init__(self, agent_name: str, error: str):
        super().__init__(f"{agent_name} is unavailable.\n{error}")


class AgentDependenciesMissing(Exception):
    def __init__(self, agent_name: str, optional_dep: str):
        super().__init__(
            f"{agent_name} is missing a dependency.\nMake sure to install optional dependencies for this agent: `pip install auto-llama[agent.{optional_dep}]`"
        )


class AgentExecutionFailed(Exception):
    def __init__(self, agent_name: str, error: str):
        super().__init__(f"{agent_name}: {error}")


class ModuleDependenciesMissing(Exception):
    def __init__(self, module_name: str, optional_dep: str):
        super().__init__(
            f"{module_name} is missing a dependency.\nMake sure to install optional dependencies for this module: `pip install auto-llama[module.{optional_dep}]`"
        )
