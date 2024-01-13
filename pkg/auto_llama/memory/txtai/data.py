from typing import Any, Callable, Iterable, TypeVar

from auto_llama import exceptions
from auto_llama.data import Content, Image, ImageSource, Article

try:
    from auto_llama_extras import text as nlp
except ImportError:
    raise exceptions.MemoryDependenciesMissing("TxtAIMemory", "txtai")


class DataSegments:
    """Work with data segments"""

    def __init__(self, segments: list[str]):
        self._segments = segments

    @classmethod
    def from_text(cls, text: str):
        """Initialize with a text by spliting it at ', '"""

        return cls(cls._text_to_segments(text))

    @classmethod
    def from_fragments(cls, fragments: list[str]):
        """Initialize with a list of text fragments by spliting thme at ', '"""

        segments: list[str] = []
        for fragment in fragments:
            segments.extend(cls._text_to_segments(fragment))

        return cls(segments)

    @classmethod
    def _text_to_segments(cls, text: str, token_start: int = 0):
        """
        Convert text to segments
        """

        segments_str = text.split(", ")
        segments = []

        for segment in segments_str:
            token_cnt = len(nlp.tokens_from_str(segment))

            segments.append(segment)
            token_start += token_cnt

        return segments

    @property
    def segments(self) -> list[str]:
        """Return all segments"""
        return self._segments

    def paragraphs(self, cnt: int):
        """Merge segments into longer paragraphs"""

        segments = self.segments

        paragraphs: list[str] = []
        for i in range(0, len(segments), cnt):
            valid_segments = segments[i : i + cnt]
            paragraphs.append(", ".join(valid_segments))

        return paragraphs

    def merge(self, split: str = "\n", max_tokens: int = 200):
        """Merge segments to text. Overlapping segments are merged"""

        merged = self._merge(self._segments, split)
        return self._trim(merged, max_tokens)

    def join(self, split: str = "\n", max_tokens: int = 200):
        """Join segments to text. Overlapping segments are NOT merged"""

        joined = self._join(self._segments, split)
        return self._trim(joined, max_tokens)

    def _merge(self, fragments: list[str], split: str = "\n") -> str:
        """Merge fragments to text. If a fragment is included in an other fragment, it is merged"""

        result = ""

        valid_indeces = set(range(len(fragments)))
        for i, fragment in enumerate(fragments):
            valid = True

            for other in (other for j, other in enumerate(fragments) if j != i and j in valid_indeces):
                if fragment in other:
                    # Fragment is already included in other fragment -> fragment is invalid
                    valid = False
                    break

            if valid:
                result += f"{fragment}{split}"
            else:
                valid_indeces.remove(i)

        return result.strip()

    def _join(self, framgents: list[str], split: str = "\n") -> str:
        """Join fragments to text. Overlapping fragments are not merged"""

        return split.join(framgents)

    def _trim(self, text: str, max_tokens: int):
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
        segments = DataSegments([f["text"] for f in el])
        text = segments.merge(split, max_tokens)

        contents.append(Article(text=text, title=el[0]["title"], src=el[0]["src"]))

    return contents
