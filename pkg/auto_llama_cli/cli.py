from argparse import ArgumentParser
from datetime import datetime

from auto_llama import Chat, ChatMessage

from ._config import CLIConfig


def print_message(message: ChatMessage, chat: Chat):
    """Print new message to console"""

    print(f"{chat.name(message.role)}: {message.message}")


def run(config: CLIConfig, chat: Chat):
    """Run assistant loop"""

    if config.start_message:
        msg = chat.append("system", config.start_message)
        print_message(msg, chat)

    while True:
        new_message = input(f"{chat.name('user')}: ")
        chat.append("user", new_message)

        objective = config.chat_converter(chat)
        agent = config.selector.run(objective)

        context = ""
        if agent:
            results = agent.run(objective)
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
        remembered_facts = config.memory.remember(objective)
        remembered_conv = config.conversation_memory.remember(objective)

        context += "\n" + "\n".join([fact.get_formatted() for fact in remembered_facts])
        chat.format_system_message(context, remembered_conv)

        # self._chat = self._llm.chat(self._chat)
        prompt = chat.prompt + f"\n{datetime.now().isoformat()} - {chat.name('assistant')}:"
        res = config.llm.completion(prompt, stopping_strings=[f"\n{chat.name('user')}", f"\n{datetime.now().year}"])
        msg = chat.append("assistant", res.strip())
        print_message(msg, chat)


def main():
    parser = ArgumentParser(description="AutoLLaMa CLI Assistant")

    parser.add_argument(
        "-c", "--config", type=str, help="Path to config file (Python file with `config=CLIConfig(...)`)"
    )

    # TODO Add verbose argument
    # parser.add_argument("-v", "--verbose", action="store_true", help="Verbose mode")

    args = parser.parse_args()

    config = CLIConfig.load(args.config)
    chat = Chat(config.system_prompt, config.roles)

    try:
        run(config, chat)
    except KeyboardInterrupt:
        # TODO Save chat history to conversation memory
        # TODO temporary save of chat history when crash
        print("\nExiting ...")
