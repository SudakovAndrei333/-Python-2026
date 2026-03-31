import sys
from types import TracebackType
from typing import Type, Literal, IO, Optional


class Redirect:
    def __init__(self, *, stdout: Optional[IO] = None, stderr: Optional[IO] = None) -> None:
        self.new_stdout = stdout
        self.new_stderr = stderr
        self.old_stdout = None
        self.old_stderr = None

    def __enter__(self):
        self.old_stdout = sys.stdout
        self.old_stderr = sys.stderr

        if self.new_stdout is not None:
            sys.stdout = self.new_stdout
        if self.new_stderr is not None:
            sys.stderr = self.new_stderr

        return self

    def __exit__(
            self,
            exc_type: Type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: TracebackType | None
    ) -> Literal[True] | None:
        if self.new_stdout is not None:
            sys.stdout = self.old_stdout
        if self.new_stderr is not None:
            sys.stderr = self.old_stderr

        return None
