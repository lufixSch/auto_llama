import os
from urllib.parse import urlparse
from argparse import ArgumentParser

from auto_llama import logger
from auto_llama.data import Article

from auto_llama_extras.text import WebTextLoader

from ._config import CLIConfig


def is_url(url: str):
    url = urlparse(url)
    return url.scheme not in ("file", "") and url.netloc


def add_data(sources: list[str], recursive: bool, config: CLIConfig):
    web_loader = WebTextLoader()

    # detect if input is a web adress, file or folder
    articles: list[Article] = []
    for source in sources:
        if is_url(source):
            articles.append(web_loader(source))
        elif os.path.exists(source):
            if os.path.isdir(source):
                # is directory
                logger.print("Is directory")
            else:
                # is file
                logger.print("Is file")

    config.memory.save(articles)


def search_data(query: str, config: CLIConfig):
    res = config.memory.remember(query)

    for article in res:
        logger.print(article.get_formatted())
        print()


def rag_main():
    parser = ArgumentParser(description="AutoLLaMa CLI RAG Interface")

    parser.add_argument(
        "-c", "--config", type=str, help="Path to config file (Python file with `config=CLIConfig(...)`)", required=True
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose mode")

    parser.add_argument("-a", "--add", nargs="*", type=str, help="List of sources, which should be added to the RAG")
    parser.add_argument("-q", "--query", type=str, help="Query for RAG")
    parser.add_argument(
        "-r", "--recursive", action="store_true", help="Recurse through a directory (if a dir is given by --add)"
    )

    args = parser.parse_args()

    logger.configure("VERBOSE" if args.verbose else "INFO")

    config = CLIConfig.load(args.config)

    if args.add:
        add_data(args.add, args.recursive, config)
    if args.query:
        search_data(args.query, config)
