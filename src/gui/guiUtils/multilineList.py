"""
This module provides a simple listbox-like widget.
"""

from tkinter import Frame, Message
from gui.guiUtils.widgetColors import ListboxColors


class MultilineList(Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.__parent = parent
        self.config(borderwidth=1, relief='solid')
        self.__lb_cols = ListboxColors(parent).lb_colors

    def append(self, item: str):
        def clicked(msg: Message):
            print(f'Should be opening: {msg.cget("text")}')  # TODO: implement handling the click event

        def hover(enter: bool, msg: Message):
            if enter:
                msg.config(bg=self.__lb_cols['selectbackground'])
            else:
                msg.config(bg=self.__lb_cols['background'])

        if not item.endswith('\n'):
            item = item + '\n'
        msg = Message(self, text=item, anchor='w', borderwidth=1, relief='solid')
        msg.pack(fill='both')
        msg.bind("<Button-1>", lambda x: clicked(msg))
        msg.bind("<Enter>", lambda x: hover(True, msg))
        msg.bind("<Leave>", lambda x: hover(False, msg))
