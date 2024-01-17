from abc import ABC, abstractmethod

from auto_llama import exceptions
from auto_llama.data import Article

HAS_DEPENDENCIES = True

# Module specific dependencies
try:
    from bs4 import BeautifulSoup
    import requests

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


class RedditPostLoader(TextLoader):
    """Load text documents from Reddit posts (Only works with links to a single reddit post)"""

    def __init__(self, seperator: str = "\n") -> None:
        super().__init__()
        self._seperator = seperator

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
