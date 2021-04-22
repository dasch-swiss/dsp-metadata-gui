"""
This module handles the project picker window of the DSP metadata application.
"""

import tkinter as tk
from tkinter.font import Font


def pick_project(root: tk.Tk):
    # CHORE: documentation
    dialog = tk.Toplevel(root)

    def on_close():
        root.update()
        root.deiconify()
        dialog.destroy()

    dialog.wm_protocol("WM_DELETE_WINDOW", on_close)
    _get_project_dialog(dialog)
    dialog.transient(root)
    dialog.lift()
    dialog.grab_set()


def _get_project_dialog(window: tk.Toplevel):
    # CHORE: documentation
    window.title("Project selection")
    window.geometry("800x500+300+200")
    window.minsize(600, 400)
    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=1)
    window.columnconfigure(1, weight=3)
    frm_recents = tk.Frame(window)
    frm_recents.grid(column=0, row=0, padx=10, pady=10, sticky="nswe")
    _get_recent_projects(frame=frm_recents)
    frm_main = tk.Frame(window, background='green')
    frm_main.grid(column=1, row=0, padx=10, pady=10, sticky="nswe")


def _get_recent_projects(frame: tk.Frame):
    lbl_header = tk.Label(frame, text="Recent Projects", anchor='w', font=Font(size=16))
    lbl_header.pack(fill=tk.X, padx=10, pady=10)
    lst_recents = tk.Listbox(frame, font=Font(size=16))
    lst_recents.pack(fill="both", padx=10, pady=10, expand=True)
    lst_recents.insert(tk.END, "TODO: implement")
