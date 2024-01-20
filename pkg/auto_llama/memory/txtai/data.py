from typing import Any, Callable, Iterable, TypeVar

from auto_llama import exceptions
from auto_llama.data import Content, Image, ImageSource, Article

try:
    from auto_llama_extras import text as nlp
    from auto_llama_extras.text import ChunkMerger
except ImportError:
    raise exceptions.MemoryDependenciesMissing("TxtAIMemory", "txtai")


def trim(text: str, max_tokens: int):
    """Trim text to max token count"""

    tokens = nlp.tokens_from_str(text)
    tokens_count = len(tokens)

    if tokens_count <= max_tokens:
        return text

    return "".join(tokens[:max_tokens])


def metadata_from_content(content: Content) -> dict:
    """
    Fetches metadata from the given content.
    """

    if isinstance(content, Image) or isinstance(content, ImageSource):
        raise NotImplementedError(f"TxtAiMemory does not support {content.__class__.__name__} content")

    data = content.serialize()

    # remove original content and return only meta data
    data.pop("text")

    return data


_T = TypeVar("_T")


def partition(pred: Callable[[_T], int], iterable: Iterable[_T], count: int = 2) -> tuple[list[_T], ...]:
    """Partition iterable into multiple groups

    Args:
        pred (Callable[[any], int | bool]): prediction after wich the iterable should be partitioned. Returns the index of the group in wich the item fits.
        iterable (Iterable): iterable
        count (int, optional): Number of partitions. Defaults to 2.
    """

    groups = tuple([[] for _ in range(count)])

    for el in iterable:
        i = int(pred(el))
        groups[i].append(el)

    return groups


def db_fragments_to_content(fragments: list[dict[str, Any]], split: str, max_tokens: int = 200) -> list[Content]:
    """
    Convert fragments from Embeddings DB list of Content objects.

    Merge overlapping segments
    """

    # Trim fragments to max_tokens
    token_cnt = 0
    for i, f in enumerate(fragments):
        tokens = nlp.tokens_from_str(f["text"])
        fragment_token_cnt = len(tokens)

        token_cnt += fragment_token_cnt
        if token_cnt >= max_tokens:
            break

    fragments = fragments[:i]

    def fragment_to_id(f: dict[str, Any]):
        return f"{f['title']}#{f['src']}"

    # Group fragments by source
    sources = list(set([fragment_to_id(f) for f in fragments]))
    items = partition(lambda f: sources.index(fragment_to_id(f)), fragments, len(sources))

    # Create article and merge grouped fragments
    contents = []
    for el in items:
        merger = ChunkMerger([f["text"] for f in el])
        text = merger.merge(split)
        text = trim(text, max_tokens)

        contents.append(Article(text=text, title=el[0]["title"], src=el[0]["src"]))

    return contents
