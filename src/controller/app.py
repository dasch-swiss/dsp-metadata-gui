from view import View


class App:
    def __init__(self) -> None:
        self._view = View(self)
        print("app instantiated")

    def run(self) -> None:
        print("run")
