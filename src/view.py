from controller.controller import Controller


class View:
    def __init__(self, controller: Controller) -> None:
        self._controller = controller
        print("view instantiated")
