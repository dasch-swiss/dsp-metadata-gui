import sys
from pathlib import Path

from tinydb import Query, TinyDB

from models import Project
from view import View


class App:
    def __init__(self) -> None:
        self._view = View(self)
        self._instantiate_db()
        print("App initialized.")

    def _instantiate_db(self) -> None:
        db_path: Path = Path.home() / ".dsp-meta" / "db.json"
        if not db_path.parent.exists():
            db_path.parent.mkdir()
            print("Database path created.")
        self._db = TinyDB(db_path)
        print(f"Database connected at: {db_path}")

    def run(self) -> None:
        while True:
            pp = self._db.all()
            projects = [Project(**p) for p in pp]
            self._view.projects_overview(projects)

    def shout_down(self) -> None:
        print("shutting down...")
        sys.exit(0)

    def add_new_project(self) -> None:
        print("requesting new project create window")
        self._view.new_project()

    def edit_project(self, shortcode: str) -> None:
        print("editing projects not yet implemented")  # TODO: implement

    def delete_project(self, shortcode: str) -> None:
        print("deleting projects not yet implemented")  # TODO: implement
