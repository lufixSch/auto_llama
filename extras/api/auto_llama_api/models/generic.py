from .base import BaseSchema


class Version(BaseSchema):
    """API Version information"""

    version: str
    message: str
