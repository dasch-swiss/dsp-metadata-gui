"""
This module handles the main window of the DSP metadata application.
"""

import tkinter as tk


def _set_up_project(root: tk.Tk, project=None):
    # CHORE: documentation
    if project is None:
        # lbl = tk.Label(root, text="No project selected", justify=CENTER)
        # lbl.pack(expand=True, fill=BOTH)
        root.withdraw()
        _pick_project(root)
        return


def _pick_project(root: tk.Tk):
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
    window.title("Project selection")
    window.geometry("800x500+300+200")
    window.minsize(600, 400)
    window.columnconfigure(0, weight=2)
    window.rowconfigure(0, weight=1)
    window.columnconfigure(1, weight=3)
    frm_recents = tk.Frame(window, background='red')
    frm_recents.grid(column=0, row=0, padx=10, pady=10, sticky="nswe")
    frm_main = tk.Frame(window, background='green')
    frm_main.grid(column=1, row=0, padx=10, pady=10, sticky="nswe")


def run():
    """
    Run the metadata application.
    """
    root = tk.Tk()
    root.title("DSP Metadata")
    root.geometry('900x600+100+100')
    _set_up_project(root)
    root.mainloop()
