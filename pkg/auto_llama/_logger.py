
class Logger:
    """Loggin class for easy and state dependent logging."""

    VERBOSE = False

    _agent_stack = []
    _agent_level_separators = ["#", "=", "-", " "]

    def start_agent(self, name: str, separator: bool = True):
        """Start an agent for logging.

        Args:
            name: Name of the agent.
            separator: If true, a separator line will be printed depending on the agent level
        """

        sep_str = None
        if separator:
            sep_str = self._agent_level_separators[max([len(self._agent_level_separators) -1, len(self._agent_stack)])]

        self._agent_stack.append(name)
        self.print("Running ...", seperator=sep_str)

    def stop_agent(self, separator: bool = True):
        """Stop the last started agent"""


        if separator:
            sep_str = self._agent_level_separators[max([len(self._agent_level_separators) -1, len(self._agent_stack) - 1])]

            self.print("", seperator=sep_str)

        self._agent_stack.pop()

    def print(
            self,
            msg: str,
            seperator: str = None,
            verbose: bool = False,
            verbose_alt: str = None,
        ):
            """Print a formatted  message to the console

            Args:
                msg (str): Message, which will be printed
                separator (str): Symbol based on which a separator will be printed before the message
                verbose (bool): Wether this is a verbose message. If True, this message will only be printed if the agent is in verbose mode
                verbose_alt (str): An alternative message to be printed if the agent is in verbose mode
            """

            if self._verbose:
                if not verbose:
                    return

                if verbose_alt:
                    msg = verbose_alt

            if seperator:
                print(f"{seperator * 30}")

            name = self._agent_stack[-1]

            if name:
                print(f"{name}: {msg}")
            else:
                print(msg)