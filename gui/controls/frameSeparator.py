from tkinter import ttk, HORIZONTAL, X


class FrameSeparator(ttk.Frame):

    def __init__(self, parent):

        super().__init__(parent)

        ttk.Separator(self, orient=HORIZONTAL).pack(fill=X)
