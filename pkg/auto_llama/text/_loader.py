from abc import ABC, abstractmethod
import os

from urllib.parse import urlparse

from auto_llama import exceptions
from auto_llama.data import Article

HAS_DEPENDENCIES = True

# Module specific dependencies
try:
    from bs4 import BeautifulSoup
    import requests
    from pypdf import PdfReader

    from ._util import merge_symbols
except (ImportError, exceptions.ExtrasDependenciesMissing):
    HAS_DEPENDENCIES = False


class TextLoader(ABC):
    """Load text documents from different sources"""

    def __init__(self) -> None:
        if not HAS_DEPENDENCIES:
            raise exceptions.ExtrasDependenciesMissing(self.__class__.__name__, "text")

    @abstractmethod
    def __call__(self, source: str) -> Article:
        """Execute loader"""

    @abstractmethod
    def is_valid(self, source: str) -> bool:
        """Check if the source is valid for this loader"""

    def batch(self, sources: list[str]) -> list[Article]:
        """Execute loader for multiple sources"""

        return [self(s) for s in sources]


class WebTextLoader(TextLoader):
    """Load text documents from the web"""

    def __init__(self, seperator: str = "\n") -> None:
        super().__init__()
        self._seperator = seperator

    def __call__(self, source: str) -> Article:
        page = requests.get(source)
        soup = BeautifulSoup(page.content, "html.parser")

        title = soup.title.string if soup.title else "HTML Page"
        content = soup.get_text(self._seperator, strip=True)
        content = merge_symbols(content, "\n")

        return Article(text=content, title=title, src=source)

    def is_valid(self, source: str) -> bool:
        url = urlparse(source)
        return url.scheme not in ("file", "") and url.netloc


class RedditPostLoader(WebTextLoader):
    """Load text documents from Reddit posts (Only works with links to a single reddit post)"""

    def __call__(self, source: str) -> Article:
        page = requests.get(source)
        soup = BeautifulSoup(page.content, "html.parser")

        # Get h1 with slot=title
        title_el = soup.find(name="h1", attrs={"slot": "title"})
        title = title_el.get_text(strip=True)

        # Get div with slot=post-media-container
        post_el = title_el.find_next(name="div", attrs={"slot": "text-body"})
        content = post_el.get_text(self._seperator, strip=True)
        content = content.rstrip("\nRead more")

        return Article(text=content, title=title, src=source)

    def is_valid(self, source: str) -> bool:
        url = urlparse(source)
        return url.scheme not in ("file", "") and url.netloc and ("reddit" in url.netloc)


class PDFLoader(TextLoader):
    """Load text documents from PDFs"""

    _ligatures_map = {
        "ﬀ": "ff",
        "ﬁ": "fi",
        "ﬂ": "fl",
        "ﬃ": "ffi",
        "ﬄ": "ffl",
        "ﬅ": "ft",
        "ﬆ": "st",
        "Ꜳ": "AA",
        "Æ": "AE",
        "ꜳ": "aa",
    }

    def __init__(self) -> None:
        super().__init__()

    def remove_hyphens(self, text: str) -> str:
        """
        This fails for:
        * Natural dashes: well-known, self-replication, use-cases, non-semantic,
                        Post-processing, Window-wise, viewpoint-dependent
        * Trailing math operands: 2 - 4
        * Names: Lopez-Ferreras, VGG-19, CIFAR-100
        """

        lines = [line.rstrip() for line in text.split("\n")]

        # Find dashes
        line_numbers = []
        for line_no, line in enumerate(lines[:-1]):
            if line.endswith("-"):
                line_numbers.append(line_no)

        # Replace
        for line_no in line_numbers:
            lines = self.dehyphenate(lines, line_no)

        return "\n".join(lines)

    def dehyphenate(self, lines: list[str], line_no: int) -> list[str]:
        next_line = lines[line_no + 1]
        word_suffix = next_line.split(" ")[0]

        lines[line_no] = lines[line_no][:-1] + word_suffix
        lines[line_no + 1] = lines[line_no + 1][len(word_suffix) :]
        return lines

    def replace_ligatures(self, text: str) -> str:
        for search, replace in self._ligatures_map.items():
            text = text.replace(search, replace)

        return text

    def __call__(self, source: str) -> Article:
        reader = PdfReader(source)

        title = ".".join(os.path.basename(source).split(".")[:-1])
        parts: list[str] = []
        content = ""

        def visitor_body(text, cm, tm, font_dict, font_size):
            y = cm[5]
            if y > 50 and y < 720:
                parts.append(text)

        for page in reader.pages:
            content += page.extract_text(visitor_text=visitor_body)

        # text = "".join(parts)
        # text = self.remove_hyphens(text)
        # text = self.replace_ligatures(text)

        content = self.remove_hyphens(content)
        content = self.remove_hyphens(content)

        return Article(content, title, source)

    def is_valid(self, source: str) -> bool:
        return os.path.exists(source) and os.path.isfile(source) and source.lower().endswith(".pdf")


class PlainTextLoader(TextLoader):
    """Load text from a plain text file"""

    def __init__(self, file_types: list[str] = ["txt", "md"]):
        super().__init__()
        self._file_types = file_types

    def __call__(self, source: str) -> Article:
        title = ".".join(os.path.basename(source).split(".")[:-1])

        with open(source, "r") as f:
            content = f.read()

        return Article(content, title, source)

    def is_valid(self, source: str) -> bool:
        return os.path.basename(source).split(".")[-1] in self._file_types
