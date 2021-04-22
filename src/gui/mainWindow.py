"""
This module handles the main window of the DSP metadata application.
"""

from gui import pickProject
import tkinter as tk


def _set_up_project(root: tk.Tk, project=None):
    # CHORE: documentation
    if project is None:
        root.withdraw()
        pickProject.pick_project(root)
        return
    # TODO: open project


def run():
    """
    Run the metadata application.
    """
    # TODO: determine if a project should be opened right away
    root = tk.Tk()
    root.title("DSP Metadata")
    root.geometry('900x600+100+100')
    _set_up_project(root)
    root.mainloop()
