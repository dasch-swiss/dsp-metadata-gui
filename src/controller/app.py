from models import Project
from view import View
import sys


class App:
    def __init__(self) -> None:
        self._view = View(self)
        print("app instantiated")

    def run(self) -> None:
        # edit_project = self._view.projects_overview([
        #     Project(shortcode="ABCD", name="test", description="lorem ipsum"),
        #     Project(shortcode="0123", name="test2", description="lorem ipsum")
        # ])
        self._view.projects_overview([])

    def shout_down(self) -> None:
        print("shutting down...")
        sys.exit(0)

    def add_new_project(self) -> None:
        print("adding projects not yet implemented")  # TODO: implement

    def edit_project(self, shortcode: str) -> None:
        print("editing projects not yet implemented")  # TODO: implement

    def delete_project(self, shortcode: str) -> None:
        print("deleting projects not yet implemented")  # TODO: implement
