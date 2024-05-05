from pathlib import Path
from typing import Any

from auto_llama_agents import Agent, AgentSelector
from auto_llama_memory import Memory
from pydantic_settings import BaseSettings, SettingsConfigDict

from auto_llama import Config, LLMInterface


class AutoLLaMaConfig(Config):
    """Config for auto_llama"""

    selector: AgentSelector
    agents: dict[str, Agent]
    memory: Memory
    llm: LLMInterface


class Settings(BaseSettings):
    AUTO_LLAMA_CONFIG_PATH: str

    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent / ".env",
        case_sensitive=True,
    )

    @classmethod
    def model_validate(
        cls: type["Settings"],
        obj: Any,
        *,
        strict: bool | None = None,
        from_attributes: bool | None = None,
        context: dict[str, Any] | None = None
    ) -> "Settings":
        return super().model_validate(obj, strict=strict, from_attributes=from_attributes, context=context)


settings = Settings.model_validate({})
auto_llama_config = AutoLLaMaConfig.load(settings.AUTO_LLAMA_CONFIG_PATH)
