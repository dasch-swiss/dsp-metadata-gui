"""
This module handles the project picker window of the DSP metadata application.
"""

import tkinter as tk
from tkinter.font import Font
from gui.guiUtils.multilineList import MultilineList


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
    frm_main = tk.Frame(window)
    frm_main.grid(column=1, row=0, padx=10, pady=10, sticky="nswe")
    _get_main(frame=frm_main)


def _get_recent_projects(frame: tk.Frame):
    # CHORE: documentation
    lbl_header = tk.Label(frame, text="Recent Projects", anchor='w', font=Font(size=16))
    lbl_header.pack(fill=tk.X, padx=10, pady=10)
    mll_recents = MultilineList(frame)
    mll_recents.pack(fill='both')
    mll_recents.append("Project 1")
    mll_recents.append("Project 2")
    mll_recents.append("Project 3")
    # TODO: get actual recent projects


def _get_main(frame: tk.Frame):
    # CHORE: documentation
    lbl_header1 = tk.Label(frame, text="DSP", font=Font(size=42))
    lbl_header1.pack(fill=tk.X, pady=(30, 0))
    lbl_header2 = tk.Label(frame, text="Metadata", font=Font(size=20))
    lbl_header2.pack(fill=tk.X, pady=(0, 30))
    frm_buttons = tk.Frame(frame)
    frm_buttons.pack()
    btn_new = tk.Button(frm_buttons, text="New Project", padx=30, command=_on_new_project)
    btn_new.pack(fill='x', pady=5)
    btn_new.config(state='disabled')
    btn_open = tk.Button(frm_buttons, text="Open Local Project", padx=30, command=_on_open_project)
    btn_open.pack(fill='x', pady=5)
    btn_open.config(state='disabled')
    btn_import = tk.Button(frm_buttons, text="Import Project", padx=30, command=_on_import_project)
    btn_import.pack(fill='x', pady=5)
    btn_import.config(state='disabled')
    btn_options = tk.Button(frm_buttons, text="Options", padx=30, command=_on_options)
    btn_options.pack(fill='x', pady=5)
    btn_options.config(state='disabled')


def _on_new_project():
    print('New project clicked')   # TODO: implement event handling


def _on_open_project():
    print('Open project clicked')   # TODO: implement event handling


def _on_import_project():
    print('Import project clicked')   # TODO: implement event handling


def _on_options():
    print('Options clicked')   # TODO: implement event handling
