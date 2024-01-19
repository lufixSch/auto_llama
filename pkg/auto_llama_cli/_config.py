from auto_llama import (
    LLMInterface,
    ConversationMemory,
    Memory,
    Agent,
    AgentSelector,
    ChatToObjectiveConverter,
    ChatRoles,
    ConfigBase,
)


class CLIConfig(ConfigBase):
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
