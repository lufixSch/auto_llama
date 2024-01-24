from __future__ import annotations

import os
import traceback
from pathlib import Path
from argparse import ArgumentParser


# import threading
from queue import Empty
from multiprocessing import JoinableQueue, Process

from auto_llama import logger, Memory
from auto_llama.data import Article

from auto_llama_extras.text import WebTextLoader, PDFLoader, PlainTextLoader, TextLoader

from ._config import CLIConfig

web_loader = WebTextLoader()
text_loader = PlainTextLoader(file_types=["md"])
pdf_loader = PDFLoader()

src_queue: JoinableQueue[tuple[str, TextLoader]] = JoinableQueue()
article_queue: JoinableQueue[Article] = JoinableQueue()


def load_articles_job(src_queue: JoinableQueue[tuple[str, TextLoader]], article_queue: JoinableQueue[Article]):
    """Load all sources in the `src_queue` with the provided loader and puts them into `article_queue`

    Can be launched multiple times with multiprocessing.
    Assumes that all sources are already in the `src_queue`
    """

    while not src_queue.empty():
        try:
            source, loader = src_queue.get_nowait()
        except Empty:
            break

        logger.print(f"Loading '{source}' with {loader.__class__.__name__}")

        try:
            article_queue.put(loader(source))
        except Exception as e:
            if logger.log_level == "VERBOSE":
                traceback.print_exc()
            logger.print(f"Unable do load '{source}' - {str(e)}", verbose_alt=f"Unable to load '{source}'")

        src_queue.task_done()


def save_article_job(memory: Memory, article_queue: JoinableQueue[Article]):
    """Save all articles in `article_queue`

    Can not be started in a separate process (Problem with GPU and multiprocessing).
    Assumes that all articles are already in the `article_queue`
    """

    while not article_queue.empty():
        article = article_queue.get_nowait()

        logger.print(f"Saving '{article.title}'")
        try:
            memory.save(article)
        except Exception as e:
            if logger.log_level == "VERBOSE":
                traceback.print_exc()
            logger.print(
                f"Unable do save '{article.title}' - {str(e)}", verbose_alt=f"Unable to load '{article.title}'"
            )

        article_queue.task_done()


def select_file_loader(source: str):
    """Select the right loader for a given file path"""

    if text_loader.is_valid(source):
        return source, text_loader
    elif pdf_loader.is_valid(source):
        return source, pdf_loader

    raise ValueError(f"'{source}' - Unsupported file type")


def expand_folder(source: Path, recursive: bool) -> list[tuple[str, TextLoader]]:
    """Recursively traverse all directories starting at `source` and return a list of all supported files with the right loader"""

    file_paths: list[tuple[str, TextLoader]] = []

    for path in source.iterdir():
        if path.is_dir():
            if path.name.startswith("."):
                continue

            if recursive:
                file_paths.extend(expand_folder(path, recursive))
            continue

        try:
            file_paths.append(select_file_loader(path.as_posix()))
        except ValueError as e:
            logger.print(str(e), verbose=True)

    return file_paths


def make_load_jobs(sources: list[str], recursive: bool, queue: JoinableQueue[tuple[str, TextLoader]]):
    """Put all supported sources with the right loader into the `queue`"""

    for source in sources:
        source.rstrip("/")

        # Add WebPage load job
        if web_loader.is_valid(source):
            queue.put_nowait((source, web_loader))

        # Add load jobs for local data
        elif os.path.exists(source):
            # Expand directories
            if os.path.isdir(source):
                for job in expand_folder(Path(source), recursive):
                    queue.put_nowait(job)

                continue

            # Make single file job
            try:
                queue.put_nowait(select_file_loader(source))
            except ValueError as e:
                logger.print(str(e))


def add_data(sources: list[str], recursive: bool, nthreads: int, config: CLIConfig):
    """Add data to memory"""

    make_load_jobs(sources, recursive, src_queue)

    for _ in range(nthreads):
        Process(target=load_articles_job, args=(src_queue, article_queue), daemon=True).start()

    # Process(target=save_article_job, args=(config.memory, article_queue), daemon=True).start()

    src_queue.join()
    logger.print("All articles loaded!", seperator="=")

    save_article_job(config.memory, article_queue)
    logger.print("All articles saved!", seperator="=")


def search_data(query: str, config: CLIConfig):
    """Search data in memory"""

    res = config.memory.remember(query, max_tokens=500, max_items=30)

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
        "-r",
        "--recursive",
        action="store_true",
        help="Recurse through a directory (if a dir is given by --add) - excludes invisible folders (.*)",
    )
    parser.add_argument(
        "-n",
        "--nthreads",
        type=int,
        default=1,
        help="Increase number of threads for loading new source data",
    )

    args = parser.parse_args()

    logger.configure("VERBOSE" if args.verbose else "INFO")

    config = CLIConfig.load(args.config)

    if args.add:
        add_data(args.add, args.recursive, args.nthreads, config)
    if args.query:
        search_data(args.query, config)
