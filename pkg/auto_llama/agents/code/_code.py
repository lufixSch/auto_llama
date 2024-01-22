from auto_llama import AgentResponse, LLMInterface, PromptTemplate, exceptions, Chat

# Agent specific dependencies
from ._code_exec import CodeExecAgent, HAS_DEPENDENCIES, HAS_DOCKER

AGENT_NAME = "CodeAgent"


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
        if not HAS_DEPENDENCIES:
            raise exceptions.AgentDependenciesMissing(AGENT_NAME, "code")
        if not HAS_DOCKER:
            raise exceptions.AgentUnavailableError(AGENT_NAME, error="Unable  to connect to docker daemon!")

        self.prompt_template = prompt_template
        self.llm = llm

        super().__init__(pkg, container_path, container_name, executor_port, verbose)

    def _run(self, objective: str) -> AgentResponse:
        prompt = self.prompt_template.template.format(
            objective=objective,
            files="\n".join([self._generate_file_prompt(file) for file in self.data.items()]),
            packages=", ".join(self.pkg),
        )

        logger.print("Prompting LLM:", seperator="-", verbose=True)
        logger.print(prompt, verbose=True)

        result = self.llm.completion(prompt, max_new_tokens=800)

        logger.print("Response:", seperator="-", verbose=True)
        logger.print(result)

        return super()._run(self, prompt + result)

    def _chat(self, chat_history: Chat) -> AgentResponse:
        try:
            objective = chat_history.last_from("user")
        except ValueError:
            raise exceptions.AgentExecutionFailed(AGENT_NAME, "No user message found in chat history")

        return self.run(objective)
