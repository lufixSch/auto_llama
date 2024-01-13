from auto_llama import Agent, AgentResponse, AgentResponseItem, LLMInterface, PromptTemplate, Memory, exceptions
from auto_llama_extras.react import ReActRunner, ReActStep
from auto_llama.data import Article

HAS_DEPENDENCIES = True

try:
    from ._search import SearchAgent
except ImportError:
    HAS_DEPENDENCIES = False


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
        if not HAS_DEPENDENCIES:
            raise exceptions.AgentDependenciesMissing(self.__class__.__name__, "research")

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
            return AgentResponse(AgentResponseItem(AgentResponseItem.POSITION.CONTEXT, steps[-1].observation))

        # Generate final answer from context, if memory is present
        # WARNING Possibly redundant with RAG in Manager

        return AgentResponse.with_same_pos(
            AgentResponseItem.POSITION.CONTEXT, [Article(step.observation) for step in steps]
        )


class MultiSearchAgent(Agent):
    """Search multiple sources for information"""

    def __init__(self, sources: list[SearchAgent], verbose=False) -> None:
        if not HAS_DEPENDENCIES:
            raise exceptions.AgentDependenciesMissing(self.__class__.__name__, "research")

        self.sources = sources

        super().__init__(verbose)

    def _run(self, query: str) -> AgentResponse:
        response = AgentResponse.empty()

        for source in self.sources:
            response.append(source.run(query).items())

        return response

    def set_memory(self, memory: Memory):
        """Set long term memory for all sources"""

        for source in self.sources:
            source.set_memory(memory)

        return super().set_memory(memory)
