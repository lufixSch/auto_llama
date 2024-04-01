"""Base classes for all api schemas"""

from pydantic import BaseModel


class BaseSchema(BaseModel):
    """Base class for API Schemas"""

    def to_clean_dict(self):
        """Convert the object to dictionary excluding unspecified fields (None)"""

        return {k: v for k, v in self.model_dump().items() if v is not None}
