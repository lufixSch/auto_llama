from datetime import datetime
from typing import Callable

from ._agent import AgentResponse
from ._selector import AgentSelector
from ._preprocessors import ChatToObjectiveConverter
from ._template import PromptTemplate
from ._chat import Chat, ChatMessage
from ._memory import Memory, ConversationMemory
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
        conversation_memory: ConversationMemory,
        information_memory: Memory,
        llm: LLMInterface,
    ):
        self._selector = selector
        self._converter = chat_converter
        self._chat = chat
        self._conversation_memory = conversation_memory
        self._information_memory = information_memory
        self._llm = llm

    # TODO Limit chat history to x items (or tokens)
    # TODO Rework this to only save mesages which are not in the history
    def _conversation_memory_handler(self, message: ChatMessage, chat: Chat):
        """Will be registerd as new chat listener to add every new chat to the conversation memory"""

        self._conversation_memory.save(Chat.from_history([message], names=chat.names))

    def start(
        self, input_handler: Callable[[Chat, "Assistant"], Chat], message_handler: Callable[[ChatMessage, Chat], None]
    ):
        """Start the assistant

        Args:
            chat_handler ((chat: Chat, assistant: Assistant, should_respond: bool) -> Chat | None): Is called every time a new message is added.
            If `should_respond` a new message/response from the user is expected
        """

        msg_handler_id = self._chat.new_message_listener(message_handler)
        memory_handler_id = self._chat.new_message_listener(self._conversation_memory_handler)

        self._run = True
        while self._run:
            self._chat = input_handler(self._chat, self)

            objective = self._converter(self._chat)
            agent = self._selector.run(objective)

            context = ""
            if agent:
                res = agent.run(objective)

                response = ""

                # Interpret agent results
                for res_type, content in res.items():
                    if res_type is AgentResponse.RESPONSE_TYPE.CONTEXT:
                        context += "\n" + content
                    if res_type is AgentResponse.RESPONSE_TYPE.CHAT:
                        self._chat.last.message += "\n" + content
                    if res_type is AgentResponse.RESPONSE_TYPE.IMG:
                        response += "\n" + f"![response image]({content})"
                    if res_type is AgentResponse.RESPONSE_TYPE.RESPONSE:
                        response += "\n" + content

                # Generate response from agent results instead of llm response
                if response:
                    self._chat.append("assistant", response)
                    continue

            # TODO Customize max tokens and max_items
            remembered_facts = self._information_memory.remember(objective)
            remembered_conv = self._conversation_memory.remember(objective)

            context += "\n" + remembered_facts
            self._chat.format_system_message(context, remembered_conv)

            self._chat = self._llm.chat(self._chat)

        # Clear new message listener
        self._chat.remove_new_message_listener(msg_handler_id)
        self._chat.remove_new_message_listener(memory_handler_id)

    def stop(self):
        """Stops assistant in the next iteration"""

        self._run = False
