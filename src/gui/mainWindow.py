"""
This module handles the main window of the DSP metadata application.
"""

from . import pickProject
import tkinter as tk
from tkinter.font import Font


def _set_up_project(root: tk.Tk, project=None):
    # CHORE: documentation
    if project is None:
        root.withdraw()
        pickProject.pick_project(root)
        return


def run():
    """
    Run the metadata application.
    """
    root = tk.Tk()
    root.title("DSP Metadata")
    root.geometry('900x600+100+100')
    _set_up_project(root)
    root.mainloop()
