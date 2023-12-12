from auto_llama import exceptions

try:
    from auto_llama import nlp
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

        return result

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
