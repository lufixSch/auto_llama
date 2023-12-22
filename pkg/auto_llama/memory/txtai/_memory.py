import os
from datetime import datetime

from auto_llama import Memory, ConversationMemory, exceptions, Chat, ChatMessage

try:
    from txtai import Embeddings
    from auto_llama import nlp

    from .data import DataSegments
except ImportError:
    raise exceptions.MemoryDependenciesMissing("TxtAIMemory", "txtai")


class TxtAIMemory(Memory):
    """Long term memory based on embeddings using txtai.

    The memory can be obtional saved to disk and loaded from disk
    """

    def __init__(self, path: str = None, paragraph_len: int = 10, data_split: str = "\n") -> None:
        """Initialize new memory

        If no path is given, changes will not be saved to disk
        """

        self.permanent = True if path is not None else False
        self.location = path
        self._paragraph_len = paragraph_len
        self._data_split = data_split

        if self.permanent:
            os.makedirs(self.location, exist_ok=True)

        self.embeddings = Embeddings(path="sentence-transformers/all-MiniLM-L6-v2", content=True)

    @classmethod
    def from_disk(cls, path: str, permanent: bool = True, paragraph_len: int = 10) -> "TxtAIMemory":
        """Loads a TxtAIMemory from disk

        If `permanent` is True, changes in the memory will be saved to the same location. If
        `permanent` is False, changes  will not be saved
        """
        memory = TxtAIMemory(path=path if permanent else None, paragraph_len=paragraph_len)
        memory.embeddings.load(path=path)

        return memory

    def to_disk(self, path: str = None) -> None:
        """Saves the memory to disk

        If no `path` is given the default path will be used.
        """

        if path:
            os.makedirs(path, exist_ok=False)
        elif self.permanent:
            path = os.path.join(self.location)
        else:
            return

        self.embeddings.save(path)

    def _preprocess(self, text: str) -> str:
        """
        Apply all preprocessing steps to the given text.
        """

        text = nlp.to_lower(text)
        text = nlp.merge_spaces(text)
        text = nlp.remove_punctuation(text)
        text = nlp.remove_specific_pos(text)
        text = nlp.lemmatize(text)
        text = nlp.num_to_word(text)

        return text

    def save(self, data: str | list[str]):
        if isinstance(data, str):
            data = [data]

        processed = [self._preprocess(el) for el in data]

        seg_data = DataSegments.from_fragments(processed)
        segments = seg_data.segments
        paragraphs = seg_data.paragraphs(self._paragraph_len)
        timestamp = datetime.now().isoformat()

        self.embeddings.upsert(
            [{"text": seg, "type": "segment", "source": None, "timestamp": timestamp} for seg in segments]
        )
        self.embeddings.upsert(
            [{"text": p, "type": "paragraph", "source": None, "timestamp": timestamp} for p in paragraphs]
        )

        self.to_disk()

    def remember(self, query: str, max_tokens: int = 500, max_items: int = 10) -> str:
        """Finds matching facts and conversations based on the query"""

        processed = self._preprocess(query)
        res: list[dict[str, str]] = self.embeddings.search(
            f"select text, type, source, timestamp FROM txtai where similar({processed})", max_items
        )

        segments = [el["text"] for el in res]
        data_seg = DataSegments(segments)
        return data_seg.merge(self._data_split, max_tokens)


class TxtAIConversationMemory(ConversationMemory):
    """Long term conversation memory based on embeddings using txtai.

    The memory can be obtional saved to disk and loaded from disk
    """

    def __init__(self, path: str = None) -> None:
        """Initialize new memory

        If no path is given, changes will not be saved to disk
        """

        self.permanent = True if path is not None else False
        self.location = path

        if self.permanent:
            os.makedirs(self.location, exist_ok=True)

        self.embeddings = Embeddings(path="sentence-transformers/all-MiniLM-L6-v2", content=True)

    @classmethod
    def from_disk(cls, path: str, permanent: bool = True, paragraph_len: int = 10) -> "TxtAIMemory":
        """Loads a TxtAIMemory from disk

        If `permanent` is True, changes in the memory will be saved to the same location. If
        `permanent` is False, changes  will not be saved
        """
        memory = TxtAIMemory(path=path if permanent else None, paragraph_len=paragraph_len)
        memory.embeddings.load(path=path)

        return memory

    def to_disk(self, path: str = None) -> None:
        """Saves the memory to disk

        If no `path` is given the default path will be used.
        """

        if path:
            os.makedirs(path, exist_ok=False)
        elif self.permanent:
            path = os.path.join(self.location)
        else:
            return

        self.embeddings.save(path)

    def save(self, chat: Chat | list[ChatMessage]):
        """Saves each 'user' and 'assistant' message to conversation memory

        WARNING: No dublication checking is done. Use `chat.clone(start, end)` to provide only new messages.
        """

        if isinstance(chat, Chat):
            messages = chat.filter(exclude_roles=["system"])
        else:
            messages = chat

        data = [
            {
                "message": msg.message,
                "name": chat.name(msg.role),
                "timestamp": msg.date.isoformat(),
            }
            for msg in messages
        ]

        self.embeddings.upsert(data)

    def remember(self, query: str, max_tokens: int = 500, max_items: int = 10) -> Chat:
        processed = self._preprocess(query)
        res: list[dict[str, str]] = self.embeddings.search(
            f"select message, name, timestamp FROM txtai where similar({processed})", max_items
        )

        segments = [
            ChatMessage(None, el["message"], datetime.fromisoformat(el["timestamp"])).to_string(el["name"])
            for el in res
        ]
        data_seg = DataSegments(segments)
        return data_seg.merge(self._data_split, max_tokens)
