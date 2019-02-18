from tkinter import ttk, LEFT, StringVar, X, TOP

import gui.config as c


class FrameScaleValue(ttk.Frame):

    def __init__(self, parent):

        super().__init__(parent)

        f = ttk.Frame(self)

        # Text field input for scale value
        string_var = StringVar()
        string_var.trace("w", lambda name, index, mode, sv=string_var: self.callback(sv))
        ttk.Label(f, text='Scale value (in metres)').pack(padx=5, pady=5, side=LEFT)
        self.entry_scale_value = ttk.Entry(f, textvariable=string_var)
        self.entry_scale_value.pack(padx=5, pady=5, side=LEFT)

        f.pack(fill=X, side=TOP)

    def callback(self, _):
        try:
            c.scale_value = float(self.entry_scale_value.get())
        except ValueError:
            pass
