from .base import BaseModel


class FileLoadOptions(BaseModel):
    """Processing options for a file upload"""

    summarize: float | None = None
    """Summaize the file (0-1, where 0 is no summary and 1 is full summary)"""

    skip_appendix: bool = False
    ocr: bool = False


class FileInfo(BaseModel):
    id: str
    title: str
