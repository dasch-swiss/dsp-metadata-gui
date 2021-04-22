import tkinter as tk


class ListboxColors:
    def __init__(self, parent) -> None:
        __listbox = tk.Listbox(parent)
        self.lb_colors = {attr: __listbox.cget(attr) for attr in (
            "background", "foreground", "disabledforeground",
            "highlightbackground", "highlightcolor",
            "selectbackground", "selectforeground"
        )}
        __listbox.destroy()
