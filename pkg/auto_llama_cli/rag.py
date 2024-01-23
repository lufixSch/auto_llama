import os
from pathlib import Path
from argparse import ArgumentParser

from auto_llama import logger
from auto_llama.data import Article

from auto_llama_extras.text import WebTextLoader, PDFLoader, PlainTextLoader

from ._config import CLIConfig

web_loader = WebTextLoader()
text_loader = PlainTextLoader()
pdf_loader = PDFLoader()


def load_file(source: str):
    if text_loader.is_valid(source):
        return text_loader(source)
    elif pdf_loader.is_valid(source):
        return pdf_loader(source)

    raise ValueError(f"'{source}' - Unsupported file type")


def load_folder(source: Path, recursive: bool) -> list[Article]:
    articles: list[Article] = []

    for path in source.iterdir():
        if path.is_dir():
            if recursive:
                articles.extend(load_folder(path, recursive))
            continue

        try:
            logger.print(f"Loading '{path.as_posix()}' as File", verbose=True)
            articles.append(load_file(path.as_posix()))
        except ValueError as e:
            logger.print(str(e), verbose=True)

    return articles


def add_data(sources: list[str], recursive: bool, config: CLIConfig):
    articles: list[Article] = []
    for source in sources:
        source = source.rstrip("/")

        # Load Web Page
        if web_loader.is_valid(source):
            logger.print(f"Loading '{source}' as WebPage")
            articles.append(web_loader(source))

        # Load local data
        elif os.path.exists(source):
            # Load supported files in directory (recursive)
            if os.path.isdir(source):
                logger.print(f"Loading '{source}' as Folder")
                articles.extend(load_folder(Path(source), recursive))

            # Load single file
            else:
                try:
                    logger.print(f"Loading '{source}' as File")
                    articles.append(load_file(source))
                except ValueError as e:
                    logger.print(str(e))

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
