import os
import shutil
import re

from auto_llama import Agent, exceptions, Chat, logger
from auto_llama.data import ImageSource
from auto_llama_agents import AgentResponse, AgentResponseItem

AGENT_NAME = "CodeExecAgent"
HAS_DEPENDENCIES = True
HAS_DOCKER = True

# Agent specific dependencies
try:
    import docker
    import pandas as pd
    from requests import post
except ModuleNotFoundError:
    HAS_DEPENDENCIES = False

if HAS_DEPENDENCIES:
    try:
        docker_client = docker.from_env()
    except docker.errors.DockerException:
        HAS_DOCKER = False


class CodeExecAgent(Agent):
    """Agent which is able to execute code written in a code block"""

    container_path: str  # = os.path.abspath(os.path.join(os.path.dirname(__file__), "code_exec"))
    allowed_filetypes = ["csv"]
    allowed_languages = ["python"]

    def __init__(
        self,
        pkg: list[str],
        container_path: str,
        container_name="code_sandbox",
        executor_port: int = 6000,
        verbose: bool = False,
    ) -> None:
        if not HAS_DEPENDENCIES:
            raise exceptions.AgentDependenciesMissing(AGENT_NAME, "code")
        if not HAS_DOCKER:
            raise exceptions.AgentUnavailableError(AGENT_NAME, error="Unable to connect to docker daemon!")

        self.pkg = pkg
        self.container_path = os.path.abspath(container_path)
        self.container_name = container_name
        self.data: dict[str, str] = {}
        self.executor_endpoint = f"http://localhost:{executor_port}"

        super().__init__(verbose)

        logger.start_agent(self.__class__.__name__, separator=False, run_msg=False)
        self._mount_container(executor_port)
        logger.stop_agent(separator=False)

    def _mount_container(self, port: int):
        """Build docker image and mount container if it doesn't run already"""

        try:
            container = docker_client.containers.get(self.container_name)
            if container.status == "running":
                logger.print("Container already running")
                return

            container.remove()
        except docker.errors.NotFound:
            pass

        logger.print("Creating Docker Container!")
        logger.print("... This might take a while ...")

        logger.print("> Building Docker Image", verbose=True)

        docker_client.images.build(path=self.container_path, tag=self.container_name)

        logger.print("> Image built successfully!", verbose=True)

        logger.print("> Starting Docker Container", verbose=True)

        # Run the container with volume mounts for data and code files
        docker_client.containers.run(
            self.container_name,
            ports={80: port},
            name=self.container_name,
            volumes={
                os.path.join(self.container_path, "static"): {
                    "bind": "/app/static",
                    "mode": "rw",
                }
            },
            detach=True,
        )

        logger.print(f"Code executor is running on {self.executor_endpoint}")

    def add_data(self, *paths: str):
        """Add data (.csv or similar) to the code executor"""

        logger.print("Adding Data!")

        data_path = os.path.join(self.container_path, "static", "files")

        for path in paths:
            basename = os.path.basename(path)
            file_type = basename.split(".")[-1].lower()

            if file_type not in self.allowed_filetypes:
                raise exceptions.AgentExecutionFailed(AGENT_NAME, f"Unsupported file type {file_type}")

            self.data[basename] = file_type

            # TODO: Move file into data folder of the container
            shutil.copy(path, data_path)

        logger.print(f"Data: {', '.join([x for x in self.data.keys()])}", verbose=True)

    def add_pkg(self, *packages: str):
        """Extend list of usable python packages"""

        self.pkg.extend(packages)

        # TODO: Add to requirements.txt and install in container

    def _extract_code(self, text: str):
        """Extract code from llm response"""

        pattern = r"```(?P<language>.*)\n(?P<code>[^`]*)\n```"
        match = re.search(pattern, text)

        if match is None:
            raise exceptions.AgentExecutionFailed(AGENT_NAME, "No code found in response")

        language = match.group("language")
        code = match.group("code").strip()

        return (language, code)

    def _generate_file_prompt(self, file: tuple[str, str]):
        """Generate prompt for file with example"""

        prompt = f"{file[0]}:"

        if file[1] == "csv":
            df = pd.read_csv(os.path.join(self.CONTAINER_PATH, "static", "files", file[0]))

            # Load header and data types of each column in the csv
            cols = [f"{col}: {df[col].dtype}" for col in df.columns]

            prompt += " | ".join(cols)
            return prompt

    def _execute_code(self, code: str):
        """Execute code in sandboxed environment and return output"""

        res = post(self.executor_endpoint, json={"code": code})

        if res.status_code != 200:
            raise exceptions.AgentExecutionFailed(AGENT_NAME, "Failed to execute code")

        res_dict = res.json()

        return (res_dict["response"], res_dict["images"])

    def _run(self, input_txt: str) -> AgentResponse:
        try:
            lang, code = self._extract_code(input_txt)
        except ValueError:
            logger.print("No valid code found in response")
            return AgentResponse(AgentResponseItem(AgentResponseItem.POSITION.CHAT, "No valid code found in response"))

        if lang not in self.allowed_languages:
            logger.print(f"Unsupported language {lang}")
            return AgentResponse.with_same_pos(
                AgentResponseItem.POSITION.CHAT,
                [
                    code,
                    f"Unsupported language {lang}",
                ],
            )

        try:
            output, images = self._execute_code(code)
        except exceptions.AgentExecutionFailed:
            logger.print("Failed to execute code")
            return AgentResponse.with_same_pos(
                AgentResponseItem.POSITION.CHAT,
                [
                    code,
                    "Failed to execute code",
                ],
            )

        return AgentResponse(
            [
                AgentResponseItem(AgentResponseItem.POSITION.CHAT, code),
                AgentResponseItem(AgentResponseItem.POSITION.CHAT, output),
                *[
                    AgentResponseItem(
                        AgentResponseItem.POSITION.RESPONSE,
                        ImageSource(
                            src=f"{self.executor_endpoint}/static/images/{img}",
                            caption=f"Output of code ```\n{code}\n```",
                        ),
                    )
                    for img in images
                ],
            ]
        )

    def _chat(self, chat_history: Chat) -> AgentResponse:
        try:
            input_txt = chat_history.last_from("user")
        except ValueError:
            raise exceptions.AgentExecutionFailed(AGENT_NAME, "No user message found in chat history")

        return self.run(input_txt)

    def __del__(self):
        logger.print_agent(self.__class__.__name__, "Stopping Docker Container!")
        try:
            container = docker_client.containers.get(self.container_name)
            container.kill()
        except docker.errors.NotFound:
            pass
