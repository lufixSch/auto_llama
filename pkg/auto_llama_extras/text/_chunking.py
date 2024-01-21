import numpy as np

from auto_llama import exceptions, ModelLoader


HAS_DEPENDENCIES = True

try:
    from spacy.language import Language
except ImportError:
    #    raise exceptions.ExtrasDependenciesMissing("nlp", "nlp")
    HAS_DEPENDENCIES = False


class TextChunker:
    """Helps to split text into sentences or groups of related sentences"""

    def __init__(self, text: str) -> None:
        if not HAS_DEPENDENCIES:
            raise exceptions.ExtrasDependenciesMissing(self.__class__.__name__, "text")

        self._text = text

        nlp = ModelLoader.get("spacy", Language)
        self._doc = nlp(self._text)

    def sentences(self) -> list[str]:
        """Splits the text into sentences."""

        sentences = [sent.text for sent in self._doc.sents]
        return sentences

    def paragraphs(self, threshold: float = 0.5, seperator: str = " "):
        """Splits the text into paragraphs, with optional overlap between them."""

        sents = [sent for sent in self._doc.sents]
        vecs = np.stack([sent.vector / sent.vector_norm for sent in sents])
        paragraphs: list[str] = [sents[0].text]

        for i, sent in enumerate(sents[1:], start=1):
            if np.dot(vecs[i], vecs[i - 1]) < threshold:
                paragraphs.append("")
                paragraphs[-1] += sent.text
            else:
                paragraphs[-1] += seperator + sent.text

        return paragraphs


class ChunkMerger:
    """Merges chunks generated with TextChunker back into one text"""

    def __init__(self, chunks: list[str]) -> None:
        if not HAS_DEPENDENCIES:
            raise exceptions.ExtrasDependenciesMissing(self.__class__.__name__, "text")

        self._chunks = chunks

    def merge(self, seperator: str = " "):
        result = ""
        valid_idx = set(range(len(self._chunks)))

        for i, chunk in enumerate(self._chunks):
            valid = True

            for other_chunk in (other for j, other in enumerate(self._chunks) if j != i and j in valid_idx):
                if chunk in other_chunk:
                    # Chunk is already included in other chunk -> chunk is invalid
                    valid = False
                    valid_idx.remove(i)
                    break

            if valid:
                result += chunk + seperator

        return result.strip(seperator)
