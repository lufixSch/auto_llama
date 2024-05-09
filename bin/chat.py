"""A simple chat cli to get startet with auto_llama

The config needs the following attributes:
Config(
  llm: LLMInterface
  agents: dict[str, Agent]
  selector: AgentSelector
  memory: Memory
  conversation_memory: ConversationMemory
  roles: dict[ChatRoles, str]
  system_prompt: str
  start_message: str
)
"""

from argparse import ArgumentParser
from datetime import datetime

from auto_llama import Chat, ChatMessage, logger, Config
from auto_llama_agents import AgentResponse


def print_message(message: ChatMessage, chat: Chat):
    """Print new message to console"""

    print(f"{chat.name(message.role)}: {message.message}", end="\n" if message.message else "")


def run(config: Config, chat: Chat):
    """Run assistant loop"""

    if config.start_message:
        msg = chat.append("system", config.start_message)
        print_message(msg, chat)

    while True:
        new_message = input(f"{chat.name('user')}: ")
        chat.append("user", new_message)

        results: AgentResponse = config.selector.run(chat)

        context = ""
        response = ""

        # Interpret agent results
        for out in results.items():
            if out.position is out.POSITION.CONTEXT:
                context += "\n" + out.to_string()
            if out.position is out.POSITION.CHAT:
                chat.last.message += "\n" + out.to_string()
            if out.position is out.POSITION.RESPONSE:
                response += "\n" + out.to_string()

        # Generate response from agent results instead of llm response
        if response:
            msg = chat.append("assistant", response)
            print_message(msg, chat)
            continue

        # TODO Customize max tokens and max_items
        remembered_facts = config.memory.remember(chat.last_from("user"), 1000, 50)
        remembered_conv = config.conversation_memory.remember(chat.last_from("user"), max_items=20)

        context += "\n" + "\n".join([fact.get_formatted() for fact in remembered_facts])
        chat.format_system_message(context, remembered_conv)

        # self._chat = self._llm.chat(self._chat)
        prompt = chat.prompt + f"\n{datetime.now().isoformat()} - {chat.name('assistant')}:"
        stream = config.llm.completion_stream(
            prompt, stopping_strings=[f"\n{chat.name('user')}", f"\n{datetime.now().year}"]
        )

        msg = chat.append("assistant", "")
        print_message(msg, chat)

        try:
            for chunk in stream:
                msg.message += chunk
                print(chunk, end="")
        except KeyboardInterrupt:
            stream.close()

        print("")  # Newline after message


if __name__ == "__main__":
    parser = ArgumentParser(description="AutoLLaMa CLI Assistant")

    parser.add_argument(
        "-c", "--config", type=str, help="Path to config file (Python file with `config=Config(...)`)", required=True
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose mode")

    args = parser.parse_args()

    logger.configure("VERBOSE" if args.verbose else "NONE")

    config = Config.load(args.config)
    chat = Chat(config.system_prompt, config.roles)

    try:
        run(config, chat)
    except KeyboardInterrupt:
        # TODO Save chat history to conversation memory
        # TODO temporary save of chat history when crash
        print("\nExiting ...")
