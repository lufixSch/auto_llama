import importlib.util
import sys
from typing import Any, Self

from .exceptions import ConfigError


class ConfigBase:
    """Config base class for easy customization"""

    def __init__(self, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __getattr__(self, name: str) -> Any:
        try:
            return getattr(self, f"{name}")
        except AttributeError:
            raise ConfigError(f"{name} is not a valid config option")

    @classmethod
    def load(cls, config_path: str) -> Self:
        """Load CLIConfig class from python file"""

        spec = importlib.util.spec_from_file_location("auto_llama_cli.user_config", config_path)
        config_module = importlib.util.module_from_spec(spec)
        sys.modules["auto_llama_cli.user_config"] = config_module
        spec.loader.exec_module(config_module)

        try:
            config: cls = getattr(config_module, "config")

            if not isinstance(config, cls):
                raise ConfigError(
                    f"""Variable `config` in {config_path} not `CLIConfig
Make sure, your config file includes an variable `config` which is an instance of `CLIConfig`"""
                )

            return config
        except AttributeError:
            raise ConfigError(
                f"Variable `config` not found in {config_path}\nMake sure, your config file includes an variable `config` which is an instance of `CLIConfig`"
            )
