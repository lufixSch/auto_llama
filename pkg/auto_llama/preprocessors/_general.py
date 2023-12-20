from auto_llama import InputPreprocessor


class TemplateInputPreprocessor(InputPreprocessor):
    """Process input by using placeholder strings

    Placeholder:
        context: Text injection point
        objective_start: Delimiter before the objective
        objective_end: Delimiter after the objective
    """

    def __init__(
        self,
        context: str = "<|context|>",
        objective_start: str = "<|objective_start|>",
        objective_end: str = "<|objective_end|>",
    ) -> None:
        self._context = context
        self._objective_start = objective_start
        self._objective_end = objective_end

    def __call__(self, input: str) -> str:
        """Extract objective from the input"""

        try:
            start_split = input.split(self._objective_start)[1]
        except IndexError:
            raise ValueError(f"Missing 'objective_start' delimiter: {self._objective_start}")

        end_elements = start_split.split(self._objective_end)
        if len(end_elements) <= 1:
            raise ValueError(f"Missing 'objective_end' delimiter: {self._objective_end}")

        return end_elements[0]

    def format(self, input: str, context) -> str:
        """Inject context into the given input and remove Objective delimiters"""

        return (
            input.replace(self._context, context)
            .replace(f"{self._objective_start}\n", "")
            .replace(self._objective_start, "")
            .replace(self._objective_end, "")
            .replace(f"{self._objective_end}\n", "")
        )
