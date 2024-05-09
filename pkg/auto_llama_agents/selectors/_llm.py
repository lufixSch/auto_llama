"""Agent selection using an LLM"""

import regex as re
from auto_llama_agents import Agent, AgentInfo, AgentResponse, AgentSelector

from auto_llama import LLMInterface, PromptTemplate


class AgentOverviewTemplate(PromptTemplate):
    """Template for displaying an overview of available agents and their capabilities"""

    def __init__(
        self,
        template: str,
        parameter_template: str,
        detection_pattern: str,
        tool_split: str = "\n\n",
        parameter_split: str = ", ",
    ) -> None:
        super().__init__(template)
        self._split = tool_split
        self._parameter_template = parameter_template
        self._parameter_split = parameter_split

        self.pattern = re.compile(detection_pattern)
        """RegEx pattern to detect the presence of an agent in the response"""

    def format(self, agents: dict[str, AgentInfo]) -> str:
        return self._split.join(
            [
                self._prompt.format(
                    name=name,
                    description=tool.description,
                    parameters=self._parameter_split.join(
                        [
                            self._parameter_template.format(name=param_name, description=param_description)
                            for param_name, param_description in tool.parameters.items()
                        ]
                    ),
                )
                for name, tool in agents.items()
            ]
        )

    def find(self, text: str):
        """Find the name of an agent and the parameters in a text"""

        matches = self.pattern.search(text)

        if not matches:
            return (None, None)

        agent_name = matches.group(1)
        param_str = matches.group(2)

        if param_str:
            param_str = param_str.strip().strip("'").strip('"')

        return (agent_name, param_str)


class AgentSelectionTemplate(AgentOverviewTemplate):
    """Template for prompting the llm to select an agent"""

    def __init__(
        self,
        template: str,
        tool_template: str,
        parameter_template: str,
        detection_pattern: str,
        tool_split: str = "\n\n",
        parameter_split: str = ", ",
    ) -> None:
        super().__init__(tool_template, parameter_template, detection_pattern, tool_split, parameter_split)

        self._base_template = template

    def format(self, chat: str, agents: dict[str, AgentInfo]) -> str:
        return self._base_template.format(tools=super().format(agents), chat=chat)


class LLMAgentSelector(AgentSelector):
    """Automatically call Agents naturally inside the conversation"""

    def __init__(
        self, tools: dict[str, Agent], llm: LLMInterface, template: AgentSelectionTemplate, max_history: int = 10
    ):
        """
        Args:
            tools (dict[str, Agent]): Dictionary of available tools with their name as key
            llm (LLMInterface): Interface to the LLM model
            template (AgentSelectionTemplate): Template for prompting the llm to select an agent
            max_history (int, optional): Maximum number of chat history items to consider. Defaults to 10.
        """

        self._tools = tools
        self._llm = llm
        self._template = template
        self._max_history = max_history

    def run(self, chat, available_agents):
        msg = chat.history[-min(self._max_history, chat.size) :]
        chat_str = "\n".join([m.to_string(chat.name(m.role)) for m in msg])

        prompt = self._template.format(chat=chat_str, agents=available_agents)
        response = self._llm.completion(prompt, stopping_strings=["\n"], max_new_tokens=200)

        agent_name, param = self._template.find(response)

        if not agent_name:
            return AgentResponse.empty()

        return self._tools[agent_name].run(param)
