from auto_llama_agents import Agent, AgentSelector


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

    def run(self, chat, available_agents):
        prompt = chat.last_from("user")
        agent = self._run(prompt, self._filter_agents(available_agents.keys(), self._tools))

        return agent.run(prompt)

    def _run(self, prompt: str, available_agents: dict[str, Agent]) -> Agent:
        for tool, c in self._commands.items():
            if prompt.startswith(c):
                return available_agents[tool]

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

    def run(self, chat, available_agents):
        prompt = chat.last_from("user")
        agent = self._run(prompt, self._filter_agents(available_agents.keys(), self._tools))

        return agent.run(prompt)

    def _run(self, prompt: str, available_agents: dict[str, Agent]) -> Agent:
        for tool, keyword in self._keywords.items():
            if keyword.lower() in prompt.lower():
                return available_agents[tool]

        return None
