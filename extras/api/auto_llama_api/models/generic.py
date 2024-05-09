from .base import BaseSchema


class Version(BaseSchema):
    """API Version information"""

    version: str
    message: str


class ListResponse(BaseSchema):
    """A list of items"""

    items: list[str]
