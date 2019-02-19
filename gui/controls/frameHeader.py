from tkinter import ttk, LEFT


class FrameHeader(ttk.Frame):

    def __init__(self, parent):

        super().__init__(parent)

        label = ttk.Label(self, text='Measure.it')
        label.config(font=('Arial', 24))
        label.pack(padx=5, pady=5, side=LEFT)
