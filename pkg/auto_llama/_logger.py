from typing import Literal


class Logger:
    """Loggin class for easy and state dependent logging."""

    _log_level: Literal["VERBOSE"] | Literal["INFO"] | Literal["NONE"] = "INFO"
    _log_file: str = None
    _agent_level_separators = ["#", "=", "-", " "]
    _seperator_len = 30

    _agent_stack = []

    @property
    def log_level(self):
        """Get the current log level."""
        return self._log_level

    @property
    def log_file(self):
        """Get the current log file path."""
        return self._log_file

    @property
    def agent_level(self):
        """Get the current agent level."""
        return max(0, len(self._agent_stack) - 1)

    def configure(
        self,
        log_level: Literal["VERBOSE"] | Literal["INFO"] | Literal["NONE"] = "INFO",
        log_file: str = None,
        agent_level_separators: list[str] = ["#", "=", "-", " "],
    ) -> "Logger":
        """Configure the logger with a verbosity level and a list of separators for the agent level."""

        self._log_level = log_level
        self._log_file = log_file
        self._agent_level_separators = agent_level_separators

        return self

    def start_agent(self, name: str, separator: bool = True, run_msg: bool = True):
        """Start an agent for logging.

        Args:
            name: Name of the agent.
            separator: If true, a separator line will be printed depending on the agent level
            run_msg: If true, a start message will be printed
        """

        sep_str = None
        self._agent_stack.append(name)

        if separator:
            sep_str = self._agent_level_separators[min([len(self._agent_level_separators) - 1, self.agent_level])]

        if run_msg:
            self.print("Running ...", seperator=sep_str)

    def stop_agent(self, separator: bool = True):
        """Stop the last started agent"""

        if not self._agent_stack:
            return

        if separator:
            sep_str = self._agent_level_separators[min([len(self._agent_level_separators) - 1, self.agent_level])]

            self.println(f"{sep_str * self._seperator_len}")

        self._agent_stack.pop()

    def print(
        self,
        msg: str,
        seperator: str = None,
        verbose: bool = False,
        verbose_alt: str = None,
    ):
        """Print a formatted  message to the console

        Automatically writes to log file

        Args:
            msg (str): Message, which will be printed
            separator (str): Symbol based on which a separator will be printed before the message
            verbose (bool): Wether this is a verbose message. If True, this message will only be printed if the agent is in verbose mode
            verbose_alt (str): An alternative message to be printed if the agent is in verbose mode
        """

        # Check log_level
        if self.log_level != "VERBOSE" and verbose:
            return

        if self.log_level == "VERBOSE" and verbose_alt:
            msg = verbose_alt

        out = ""

        # Add seperator
        if seperator:
            out += f"{seperator * self._seperator_len}\n"

        # Add indentation
        out += "".join(["  " for _ in range(self.agent_level)])

        # Add agent name
        name = self._agent_stack[-1] if self._agent_stack else None
        if name:
            out += f"{name}: "

        # Add message
        out += msg

        # Print to console and file
        self.println(out, verbose)

    def println(self, msg: str, verbose: bool = False):
        """Basic print function for simple messages

        Automatically writes to log file
        """

        # Print to console and file
        self.write_file(msg)

        if (self.log_level == "INFO" and not verbose) or self.log_level == "VERBOSE":
            print(msg)

    def print_agent(
        self,
        name: str,
        msg: str,
        seperator: str = None,
        verbose: bool = False,
        verbose_alt: str = None,
    ):
        """Print a formatted  message to the console in the name of a specific agent

        Alias for:
        Logger.start_agent(name, separator=False, run_msg=False)
        Logger.print(msg, seperator, verbose, verbose_alt)
        Logger.stop_agent(separator=False)

        Args:
            msg (str): Message, which will be printed
            separator (str): Symbol based on which a separator will be printed before the message
            verbose (bool): Wether this is a verbose message. If True, this message will only be printed if the agent is in verbose mode
            verbose_alt (str): An alternative message to be printed if the agent is in verbose mode
        """

        self.start_agent(name, separator=False, run_msg=False)
        self.print(msg, seperator, verbose, verbose_alt)
        self.stop_agent(separator=False)

    def write_file(self, msg: str):
        """Append a message to the log file"""

        if not self._log_file:
            return

        with open(self.log_file, "a") as file:
            file.write(msg + "\n")


logger = Logger()
