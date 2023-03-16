from typing import Any
from controller.controller import Controller

import PySimpleGUI as sg

from models import Project

font = ("Arial", 16)


class View:
    def __init__(self, controller: Controller) -> None:
        self._controller = controller
        self._projects_overview_window = None
        self._new_project_window = None

    def _make_projects_overview_window(self, projects: list[Project]) -> sg.Window:
        layout = self._get_projects_layout(projects)
        return sg.Window(
            title="DSP Metadata",
            layout=layout,
            margins=(50, 30),
            font=font,
            element_padding=10,
            resizable=True,
            size=(800, 600),
            finalize=True
        )

    def _get_project_row(self, p: Project) -> list[sg.Element]:
        content = [[
            sg.Text(p.name),
            sg.Text(f"({p.shortcode})"),
            sg.VerticalSeparator(),
            sg.Text(p.description, expand_x=True),
            sg.VerticalSeparator(),
            sg.Button("Edit", key=f"-ED-{p.shortcode}"),
            sg.Button("Delete", key=f"-DEL-{p.shortcode}")
        ]]
        return [sg.Frame("", content, expand_x=True)]

    def _get_projects_layout(self, projects: list[Project]) -> list[list[sg.Element]]:
        rows: list[list[sg.Element]] = [[sg.Text("No Projects added yet")]]
        if projects:
            rows = [self._get_project_row(p) for p in projects]
        rows.append([sg.Push(), sg.Button("Add new Project", key="-NEW-")])
        return rows

    def _make_new_project_window(self) -> sg.Window:
        layout = [
            [
                sg.Button("blah")
            ],
            [
                sg.Button("Back"),
                sg.ProgressBar(100, expand_x=True),
                sg.Button("Back"),
            ]
        ]
        return sg.Window(
            title="DSP Metadata",
            layout=layout,
            margins=(50, 30),
            font=font,
            element_padding=10,
            resizable=True,
            size=(800, 600),
            finalize=True
        )

    def _read_event(self) -> tuple[sg.Window, str, dict[str | int, Any]]:
        w = sg.read_all_windows()
        assert isinstance(w, tuple)
        window, event, values = w
        assert window
        if event == sg.WIN_CLOSED:
            self._controller.shout_down()
        assert isinstance(event, str)
        assert isinstance(values, dict)
        return window, event, values

    def projects_overview(self, projects: list[Project]) -> None:
        self._projects_overview_window = self._make_projects_overview_window(projects)
        while True:
            _, event, values = self._read_event()
            if event == "-NEW-":
                self._controller.add_new_project()
                break
            if event.startswith("-ED-"):
                shortcode = event.removeprefix("-ED-")
                self._controller.edit_project(shortcode)
                break
            if event.startswith("-DEL-"):
                shortcode = event.removeprefix("-DEL-")
                self._controller.delete_project(shortcode)
                break
            print(f"Unhandled event: {event} ({values})")
        if self._projects_overview_window:
            self._projects_overview_window.hide()

    def new_project(self) -> None:
        self._new_project_window = self._make_new_project_window()
        while True:
            _, event, values = self._read_event()
            print(event, values)
            break
        if self._new_project_window:
            self._new_project_window.close()
        if self._projects_overview_window:
            self._projects_overview_window.un_hide()

    # def _get_some_layout(self) -> list[list[Any]]:
    #     self._progress_bar = sg.ProgressBar(100, size=(20, 20), expand_x=True)
    #     self._btn_previous = sg.Button("Previous", disabled=True)
    #     self._btn_next = sg.Button("Next")
    #     return [
    #         [sg.Text("TODO: Title")],
    #         [sg.HorizontalSeparator()],
    #         [sg.Text("TODO: Content")],
    #         [sg.HorizontalSeparator()],
    #         [
    #             self._btn_previous,
    #             self._progress_bar,
    #             self._btn_next
    #         ]
    #     ]

    # def _handle_window_event(self, event: str | None) -> None:
    #     match event:
    #         case "Next":
    #             self._step += 1
    #             self._progress_bar.update(self._step)
    #         case _:
    #             print(f"unhandled event: {event}")
    #             pass
    #     self._btn_previous.update(disabled=self._step <= 0)

    # def main_loop(self) -> None:
    #     layout = self._get_some_layout()
    #     font = ("Arial", 16)
    #     step = 0
    #     window = sg.Window(
    #         title="Hello World",
    #         layout=layout,
    #         margins=(50, 30),
    #         font=font,
    #         element_padding=10,
    #         resizable=True,
    #         size=(800, 600)
    #     )
    #     while True:
    #         w = window.read()
    #         assert isinstance(w, tuple)
    #         event, values = w
    #         if event == sg.WIN_CLOSED:
    #             print("window closed")
    #             break
    #         match event:
    #             case "Next":
    #                 step += 1
    #                 self._progress_bar.update(step)
    #             case _:
    #                 print(f"unhandled event: {event}")
    #                 pass
    #         self._btn_previous.update(disabled=step <= 0)
