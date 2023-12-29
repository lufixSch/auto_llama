from datetime import datetime
from typing import Callable

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
        max_messages: int = 10,
    ):
        self._selector = selector
        self._converter = chat_converter
        self._chat = chat
        self._conversation_memory = conversation_memory
        self._information_memory = information_memory
        self._llm = llm
        self._max_messages = max_messages

    def _conversation_memory_handler(self, message: ChatMessage, chat: Chat):
        """Will be registerd as new chat listener to add every new chat to the conversation memory"""

        if self._max_messages <= 0:
            return

        removed = self._chat.trunc(self._max_messages)

        if removed:
            self._conversation_memory.save(Chat.from_history(removed, names=chat.names))

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
                for out in res.items():
                    if out.position is out.POSITION.CONTEXT:
                        context += "\n" + out.to_string()
                    if out.position is out.POSITION.CHAT:
                        self._chat.last.message += "\n" + out.to_string()
                    if out.position is out.POSITION.RESPONSE:
                        response += "\n" + out.to_string()

                # Generate response from agent results instead of llm response
                if response:
                    self._chat.append("assistant", response)
                    continue

            # TODO Customize max tokens and max_items
            remembered_facts = self._information_memory.remember(objective)
            remembered_conv = self._conversation_memory.remember(objective)

            context += "\n" + "\n".join([fact.get_formatted() for fact in remembered_facts])

            print(context)

            self._chat.format_system_message(context, remembered_conv)

            # self._chat = self._llm.chat(self._chat)
            prompt = self._chat.prompt + f"\n{datetime.now().isoformat()} - {self._chat.name('assistant')}:"
            res = self._llm.completion(
                prompt, stopping_strings=[f"\n{self._chat.name('user')}", f"\n{datetime.now().year}"]
            )
            self._chat.append("assistant", res.strip())

        # Clear new message listener
        self._chat.remove_new_message_listener(msg_handler_id)
        self._chat.remove_new_message_listener(memory_handler_id)

    def stop(self):
        """Stops assistant in the next iteration"""

        self._run = False
