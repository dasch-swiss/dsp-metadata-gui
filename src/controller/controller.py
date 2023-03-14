from typing import Protocol


class Controller(Protocol):
    def run(self) -> None:
        ...
