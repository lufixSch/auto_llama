from argparse import ArgumentParser

import gradio as gr

from auto_llama import Chat, ChatMessage

from ._config import GUIConfig

config: GUIConfig = None
chat: Chat = None


def send_message(msg: str):
    chat.append("user", msg)


def main():
    global config, chat

    parser = ArgumentParser(description="AutoLLaMa GUI")

    parser.add_argument(
        "-c", "--config", help="Path to config file (Python file with `config=CLIConfig(...)`)", required=True
    )
    parser.add_argument("--listen", action="store_true", help="Make the GUI available in your network")

    # TODO Add verbose argument
    # parser.add_argument("-v", "--verbose", action="store_true", help="Verbose mode")

    args = parser.parse_args()
    print(args)

    config = GUIConfig.load(args.config)
    chat = Chat(config.system_prompt, config.roles)

    with gr.Blocks(theme=gr.themes.Soft()) as app:
        gr.Markdown("# AutoLLaMa")

        for message in chat.history:
            with gr.Blocks():
                if message.role == "system":
                    gr.Textbox(f"**System:** {message.message}")
                elif message.role == "user":
                    gr.Textbox(f"**User:** {message.message}")

        # Input fields
        input_field = gr.Textbox(
            lines=config.max_input_lines,
            placeholder="Enter your message...",
            label="Message",
        )

        # Send button
        submit_button = gr.Button("Send")

        submit_button.click(
            fn=send_message,
            inputs=input_field,
            outputs=[],
        )

    app.launch(share=args.listen)
