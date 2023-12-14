from auto_llama import AgentManager, Agent, AgentResponse

class CommandAgentManager(AgentManager):
    """Detect requested agent using a keyword/command. Prompt has to start with it"""

    def __init__(self, tools: dict[str, Agent], commands: dict[str, str]):
        """
        Arguments:
            tools (dict[str, Agent]): Dictionary of available tools with their name as key
            commands (dict[str, str]): Keywords for each tool with the tool name as key.
        """

        self._tools = tools
        self._commands = commands


    def _run(self, prompt: str) -> AgentResponse:
        for tool, c in self._commands.items():
            if prompt.startswith(c):
                return self._tools[tool].run(prompt)

        return AgentResponse.empty()