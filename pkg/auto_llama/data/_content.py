from abc import ABC, abstractmethod
from PIL import Image as PILImage
import io

from ._serializable import Serializable


class Content(Serializable, ABC):
    """Base class for content"""

    def __init__(self, **kwargs) -> None:
        for name, val in kwargs.items():
            setattr(self, name, val)

    @abstractmethod
    def get_content(self) -> str:
        """Return a string representation of the content (only the explicit content, no metadata)"""

    @abstractmethod
    def get_formatted(self) -> str:
        """(Markdown) formatted content (with meta data depending on the content type)"""

    def __str__(self) -> str:
        """Alias for `get_formatted`"""

        return self.get_formatted()


class Article(Content):
    """Representation of a single article"""

    def __init__(self, text: str, title: str = None, src: str = None, **kwargs) -> None:
        self.title = title
        self.src = src
        self.text = text

        super().__init__(**kwargs)

    def get_content(self) -> str:
        return self.text

    def get_formatted(self) -> str:
        title_str = f"# {self.title}"
        source_str = f"Source: {self.src}"

        return (f"{title_str}\n" if self.title else "") + self.text + (f"\n{source_str}" if self.src else "")

    def serialize(self) -> dict:
        return self.__dict__.copy()

    @classmethod
    def deserialize(cls, data: dict) -> Serializable:
        return cls(**data)


class ImageSource(Content):
    """Representation of an image as source path/url"""

    def __init__(self, src: str, caption: str = "", **kwargs) -> None:
        self.src = src
        self.caption = caption

        super().__init__(**kwargs)

    def get_content(self) -> str:
        return self.src

    def get_formatted(self) -> str:
        return f"![{self.caption}]({self.src})"

    def serialize(self) -> dict:
        return self.__dict__.copy()

    @classmethod
    def deserialize(cls, data: dict) -> Serializable:
        return cls(**data)


class Image(Content):
    """Representation of an image with caption"""

    def __init__(self, img: PILImage, caption: str, **kwargs) -> None:
        self.img = img
        self.caption = caption

    def get_content(self) -> str:
        """Return the image as binary data, so it can be saved to a file"""

        img_byte_arr = io.BytesIO()
        self.img.save(img_byte_arr, format="PNG")

        return str(img_byte_arr.getvalue())

    def get_formatted(self) -> str:
        """Returns the caption of the image"""

        # TODO: save image to tmp file and add link
        return self.caption

    def serialize(self) -> dict:
        img_str = self.get_content()

        return {**self.__dict__.copy(), "img": img_str, "caption": self.caption}

    @classmethod
    def deserialize(cls, data: dict) -> Serializable:
        img_bytes = data.pop("img")
        img = PILImage.open(io.BytesIO(img_bytes))

        return cls(img=img, **data)
