from auto_llama import AgentSelector, Agent


class CommandAgentSelector(AgentSelector):
    """Detect requested agent using a command. Prompt has to start with it"""

    def __init__(self, tools: dict[str, Agent], commands: dict[str, str]):
        """
        Args:
            tools (dict[str, Agent]): Dictionary of available tools with their name as key
            commands (dict[str, str]): Command for each tool with the tool name as key.
        """

        self._tools = tools
        self._commands = commands

    def _run(self, prompt: str) -> Agent:
        for tool, c in self._commands.items():
            if prompt.startswith(c):
                return self._tools[tool]

        return None


class KeywordAgentSelector(AgentSelector):
    """Detect requested agent by searching for a keyword"""

    def __init__(self, tools: dict[str, Agent], keywords: dict[str, str]) -> None:
        """
        Args:
            tools (dict[str, Agent]): Dictionary of available tools with their name as key
            keywords (dict[str, str]): Keywords for each tool with the tool name as key.
        """

        self._tools = tools
        self._keywords = keywords

    def _run(self, prompt: str) -> Agent:
        for tool, keyword in self._keywords.items():
            if keyword.lower() in prompt.lower():
                return self._tools[tool]

        return None
