from typing import Protocol


class Controller(Protocol):
    def run(self) -> None:
        ...

    def shout_down(self) -> None:
        ...

    def add_new_project(self) -> None:
        ...

    def edit_project(self, shortcode: str) -> None:
        ...

    def delete_project(self, shortcode: str) -> None:
        ...
