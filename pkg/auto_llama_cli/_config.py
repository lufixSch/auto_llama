import importlib.util
import sys

from auto_llama import (
    LLMInterface,
    ConversationMemory,
    Memory,
    Agent,
    AgentSelector,
    ChatToObjectiveConverter,
    ChatRoles,
)
from .exceptions import ConfigError


class CLIConfig:
    """CLI Config class"""

    def __init__(
        self,
        llm: LLMInterface,
        agents: dict[str, Agent],
        selector: AgentSelector,
        chat_converter: ChatToObjectiveConverter,
        memory: Memory,
        conversation_memory: ConversationMemory,
        roles: dict[ChatRoles, str],
        system_prompt: str,
        start_message: str = None,
    ) -> None:
        self.llm = llm
        self.conversation_memory = conversation_memory
        self.memory = memory
        self.agents = agents
        self.selector = selector
        self.chat_converter = chat_converter
        self.system_prompt = system_prompt
        self.roles = roles
        self.start_message = start_message

    @classmethod
    def load(cls, config_path: str) -> "CLIConfig":
        """Load CLIConfig class from python file"""

        spec = importlib.util.spec_from_file_location("auto_llama_cli.user_config", config_path)
        config_module = importlib.util.module_from_spec(spec)
        sys.modules["auto_llama_cli.user_config"] = config_module
        spec.loader.exec_module(config_module)

        try:
            config: CLIConfig = getattr(config_module, "config")

            if not isinstance(config, CLIConfig):
                raise ConfigError(
                    f"""Variable `config` in {config_path} not `CLIConfig
Make sure, your config file includes an variable `config` which is an instance of `CLIConfig`"""
                )

            return config
        except AttributeError:
            raise ConfigError(
                f"Variable `config` not found in {config_path}\nMake sure, your config file includes an variable `config` which is an instance of `CLIConfig`"
            )
