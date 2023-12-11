from auto_llama import Agent, AgentResponse, LLMInterface, PromptTemplate, exceptions
from auto_llama.react import ReActRunner, ReActStep

AGENT_NAME = "ResearchAgent"

try:
    from .search import SearchAgent
except ImportError:
    raise exceptions.AgentDependenciesMissing(AGENT_NAME, "research")


class ResearchPromptTemplate(PromptTemplate):
    """Prompt template for a COT research process

    Parameters:
        objective (str): Research goal/objective
        tools (list[str]): Available tools for research
    """

    def format(self, objective: str, tools: list[str]):
        return super().format(objective=objective, tools=", ".join(tools))


class ResearchAgent(Agent):
    """Thoroughly research a topic using different sources and and a COT process"""

    def __init__(
        self,
        prompt_template: ResearchPromptTemplate,
        llm: LLMInterface,
        tools: dict[str, SearchAgent],
        max_iterations: int = 10,
        verbose=False,
    ) -> None:
        self.prompt_template = prompt_template
        self.llm = llm
        self.tools = tools
        self.max_iter = max_iterations

        self.runner = ReActRunner(self._step)

        super().__init__(verbose)

    def _step(self, i: int, steps: list[ReActStep]) -> ReActStep:
        """Single research step"""

        self.print(f"Iteration {i+1} of {self.max_iter}", seperator="+")

        this_step = steps[-1]
        if this_step.is_final:
            self.print("Found final answer", verbose=True, verbose_alt=f"Found final answer: {this_step.observation}")
            return steps

        for name, tool in self.tools.items():
            if name not in this_step.action:
                break

            results = tool.run(this_step.action_input)
            steps[-1].observation = "\n".join(results.values())

        return steps

    def _run(self, input: str) -> AgentResponse:
        initial_prompt = self.prompt_template.format(objective=input, tools=list(self.tools.keys()))

        steps = self.runner.run(initial_prompt, self.max_iter)

        if steps[-1].is_final:
            return AgentResponse(AgentResponse.RESPONSE_TYPE.CONTEXT, steps[-1].observation)

        return AgentResponse.with_same_type(AgentResponse.RESPONSE_TYPE.CONTEXT, [step.observation for step in steps])
