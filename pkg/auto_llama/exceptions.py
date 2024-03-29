"""Custom exceptions for AutoLLaMa"""


class AgentUnavailableError(Exception):
    def __init__(self, agent_name: str, error: str):
        super().__init__(f"{agent_name} is unavailable.\n{error}")


class AgentExecutionFailed(Exception):
    def __init__(self, agent_name: str, error: str):
        super().__init__(f"{agent_name}: {error}")


class DependenciesMissing(Exception):
    def __init__(self, name: str, group_name: str, dep_name: str) -> None:
        super().__init__(
            f"{name} is missing a dependency.\nMake sure to install optional dependencies for this agent: `pip install auto-llama[{group_name}.{dep_name}]`"
        )


class AgentDependenciesMissing(DependenciesMissing):
    def __init__(self, agent_name: str, dep_name: str):
        super().__init__(agent_name, "agent", dep_name)


class ExtrasDependenciesMissing(DependenciesMissing):
    def __init__(self, module_name: str, dep_name: str) -> None:
        super().__init__(module_name, "extras", dep_name)


class LLMDependenciesMissing(DependenciesMissing):
    def __init__(self, llm_name: str, dep_name: str) -> None:
        super().__init__(f"{llm_name}", "llm", dep_name)


class MemoryDependenciesMissing(DependenciesMissing):
    def __init__(self, memory_name: str, dep_name: str) -> None:
        super().__init__(memory_name, "memory", dep_name)


class SelectorDependenciesMissing(DependenciesMissing):
    def __init__(self, selector_name: str, dep_name: str) -> None:
        super().__init__(selector_name, "selector", dep_name)


class PreprocessorDependenciesMissing(DependenciesMissing):
    def __init__(self, preprocessor_name: str, dep_name: str) -> None:
        super().__init__(preprocessor_name, "preprocessor", dep_name)


class ModelMissing(Exception):
    def __init__(self, model_group: str) -> None:
        super().__init__(
            f"Ressources missing!\nMake sure to download all neccessary ressources for {model_group}: `python bin/{model_group}_ressources`"
        )


class ConfigError(Exception):
    """Error raised when loading the config fails"""
