from typing import Callable

from ._agent import AgentResponse
from ._selector import AgentSelector
from ._preprocessors import ChatToObjectiveConverter
from ._template import PromptTemplate
from ._chat import Chat
from ._memory import Memory
from ._llm import LLMInterface


class AssistantSystemMessage(PromptTemplate):
    """Prompt template for a chat bot system message

    Parameters:
        assistant (str): Name of the assistant
        name (str): Name of the user
        context (list[str]): Aditional context which should be added to the system message
        chat_history (Chat): Old chat history, which should be added to the system message
    """

    def format(self, assistant: str, name: str, context: list[str], chat_history: Chat):
        return super().format(
            assistant=assistant, name=name, context="\n".join(context), chat_history=chat_history.prompt
        )


class Assistant:
    """High level interface which allows communication with an LLM driven chatbot with the ability to use agents"""

    _run = False

    def __init__(
        self,
        selector: AgentSelector,
        chat_converter: ChatToObjectiveConverter,
        chat: Chat,
        chat_memory: Memory,
        facts_memory: Memory,
        llm: LLMInterface,
    ):
        self._selector = selector
        self._converter = chat_converter
        self._chat = chat
        self._chat_memory = chat_memory
        self._facts_memory = facts_memory
        self._llm = llm

    def start(self, chat_handler: Callable[[Chat, "Assistant", bool], Chat | None]):
        """Start the assistant

        Args:
            chat_handler ((chat: Chat, assistant: Assistant, should_respond: bool) -> Chat | None): Is called every time a new message is added.
            If `should_respond` a new message/response from the user is expected
        """

        self._chat = chat_handler(self._chat, self, True)

        self._run = True
        while self._run:
            # TODO Add chat memory (save, remember)
            # TODO Add facts memory (remember)

            objective = self._converter(self._chat)
            agent = self._selector.run(objective)

            should_run_llm = True
            if agent:
                res = agent.run(objective)

                context = ""
                response = ""

                for res_type, content in res.items():
                    if res_type is AgentResponse.RESPONSE_TYPE.CONTEXT:
                        context += "\n" + content
                    if res_type is AgentResponse.RESPONSE_TYPE.CHAT:
                        self._chat.last.message += "\n" + content
                    if res_type is AgentResponse.RESPONSE_TYPE.IMG:
                        response += "\n" + f"![response image]({content})"
                    if res_type is AgentResponse.RESPONSE_TYPE.RESPONSE:
                        response += "\n" + content

                if response:
                    self._chat.append("assistant", response)
                    should_run_llm = False

            if should_run_llm:
                self._chat = self._llm.chat(self._chat)

            self._chat = chat_handler(self._chat, True)

    def stop(self):
        """Stops assistant in the next iteration"""

        self._run = False
