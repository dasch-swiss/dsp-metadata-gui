from controller.controller import Controller

import PySimpleGUI as sg


class View:
    def __init__(self, controller: Controller) -> None:
        self._controller = controller
        print("view instantiated")

    def main_loop(self) -> None:
        sg.Window(title="Hello World", layout=[[]], margins=(100, 50)).read()
