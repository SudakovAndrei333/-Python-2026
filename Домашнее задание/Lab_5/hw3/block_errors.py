from typing import Collection, Type
from types import TracebackType


class BlockErrors:
    def __init__(self, errors: Collection) -> None:
        self.errors = errors

    def __enter__(self) -> None:
        pass

    def __exit__(
            self,
            exc_type: Type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: TracebackType | None
    ) -> bool | None:
        if exc_type is None:
            return None
        if issubclass(exc_type, tuple(self.errors)):
            return True
        return None
    