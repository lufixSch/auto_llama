from auto_llama import AgentResponse, LLMInterface, PromptTemplate, exceptions, Chat

AGENT_NAME = "CodeAgent"

# Agent specific dependencies
try:
    from .code_exec import CodeExecAgent
except ModuleNotFoundError:
    raise exceptions.AgentDependenciesMissing(AGENT_NAME, "code")
except exceptions.AgentDependenciesMissing:
    raise exceptions.AgentDependenciesMissing(AGENT_NAME, "code")


class CodePromptTemplate(PromptTemplate):
    """Prompt template for writing code based on a given objective.

    Parameters:
        objective (str): Objective of the code, which should be generated
        files (list[str]):  list of files which can be accessed by the CodeAgent with file preview
        packages (list[str]): list of packages which the CodeAgent can access
    """

    def format(self, objective: str, files: list[str], packages: list[str]) -> str:
        return super().format(objective=objective, files="\n".join(files), packages=", ".join(packages))


class CodeAgent(CodeExecAgent):
    """Agent which is able to generate and execute code based on a objective"""

    def __init__(
        self,
        prompt_template: CodePromptTemplate,
        llm: LLMInterface,
        pkg: list[str],
        container_path: str,
        container_name="code_sandbox",
        executor_port: int = 6000,
        verbose: bool = False,
    ) -> None:
        self.prompt_template = prompt_template
        self.llm = llm

        super().__init__(pkg, container_path, container_name, executor_port, verbose)

    def _run(self, objective: str) -> AgentResponse:
        prompt = self.prompt_template.template.format(
            objective=objective,
            files="\n".join([self._generate_file_prompt(file) for file in self.data.items()]),
            packages=", ".join(self.pkg),
        )

        self.print("Prompting LLM:", seperator="-", verbose=True)
        self.print(prompt, verbose=True)

        result = self.llm.completion(prompt, max_new_tokens=800)

        self.print("Response:", seperator="-", verbose=True)
        self.print(result)

        return super()._run(self, prompt + result)

    def _chat(self, chat_history: Chat) -> AgentResponse:
        try:
            objective = chat_history.last("user")
        except ValueError:
            raise exceptions.AgentExecutionFailed(AGENT_NAME, "No user message found in chat history")

        return self.run(objective)
