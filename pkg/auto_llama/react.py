"""ReAct Framework"""

from typing import Callable, TypeAlias, Literal
import re

from ._llm import LLMInterface

ReActKeywords: TypeAlias = Literal["thought", "action", "input", "observation", "final"]


class ReActStep:
    """One step of a ReAct loop"""

    _is_final = False
    _observation = None

    def __init__(
        self,
        response: str,
        keywords: dict[ReActKeywords, str] = {
            "thought": "thought",
            "action": "action",
            "input": "input",
            "observation": "observation",
            "final": "final",
        },
    ) -> None:
        """Parse LLM response int a ReAct step

        If the response is a final step, `is_final` is set to True and `observation` contains the final answer
        """

        # Ensure only one Thought process
        trunc_res = response.split(keywords["observation"])[0].strip()

        # Be the final step if “final” is in the response
        # Set final answer as observation
        if keywords["final"] in trunc_res:
            self._observation = trunc_res.split(keywords["final"])[-1]
            self._is_final = True
            return

        # Match action and action input
        regex = rf"\s*\d*\s*:(.*?)\n{keywords['action']}\s*\d*\s*:(.*?)\n{keywords['input']}\s*\d*\s*:[\s]*(.*)"
        match = re.search(regex, trunc_res, re.DOTALL)

        # Be the final step if no action is found
        # Set final answer as observation
        if not match:
            self._is_final = True
            return

        self._thought = match.group(1).strip()
        self._action = match.group(2).strip()
        self._action_input = match.group(3).strip()

    @property
    def is_final(self) -> bool:
        return self._is_final

    @property
    def thought(self) -> str:
        if self.is_final:
            raise ValueError("No Thought process in the final step")

        return self._thought

    @property
    def action(self) -> str:
        if self.is_final:
            raise ValueError("No action in the final step")

        return self._action

    @property
    def action_input(self) -> str:
        if self.is_final:
            raise ValueError("No action input in the final step")

        return self._action_input

    @property
    def observation(self) -> str:
        if not self._observation:
            raise ValueError("Observation must be set before it can be accessed")

        return self._observation

    @observation.setter
    def observation(self, observation: str):
        self._observation = observation


class ReActRunner:
    """ReAct loop with customizable logic"""

    def __init__(
        self,
        llm: LLMInterface,
        step_cb: Callable[[int, list[ReActStep]], ReActStep],
        keywords: dict[ReActKeywords, str] = {
            "thought": "thought",
            "action": "action",
            "input": "input",
            "observation": "observation",
            "final": "final",
        },
    ) -> None:
        """
        Args:
            llm (LLMInterface): The LLM model to use for generating responses.
            step_cb (Callable[[int, list[ReActStep]], ReActStepStep]): Callback function to implement custom logic on each ReAct loop step.
            Will also be called on the final step!
            keywords (dict[ReActKeywords, str]): Keywords to match for in the ReAct LLM response.
        """

        self.llm = llm
        self.step_cb = step_cb
        self.keywords = keywords

    def _create_prompt(self, prev_prompt: str, step: ReActStep) -> str:
        """Create prompt for the next step based on the current step"""

        return f"{prev_prompt.rstrip()}\n{step.thought}\n{step.action}\n{step.action_input}\n{step.observation}\n"

    def run(self, initial_prompt: str, max_iterations: int) -> list[ReActStep]:
        """Run the ReAct loop"""

        prompt = initial_prompt
        steps: list[ReActStep] = []
        for i in max_iterations:
            prompt = self._create_prompt(prompt, steps[-1])
            response = self.llm.completion(prompt)
            this_step = ReActStep(response, self.keywords)

            steps.append(this_step)

            # Resolve action for this step
            steps = self.step_cb(i, steps)

            if this_step.is_final:
                break

        return steps
