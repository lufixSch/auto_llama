class PromptTemplate:
    """Generic template for prompts"""

    _prompt: str

    def __init__(self, template: str) -> None:
        self._prompt = template

    def format(self, **kwargs) -> str:
        return self._prompt.format(**kwargs)
