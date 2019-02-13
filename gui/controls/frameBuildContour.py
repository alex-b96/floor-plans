from tkinter import ttk, LEFT


class FrameBuildContour(ttk.Frame):

    def __init__(self, parent):

        super().__init__(parent)

        button_build_contour = ttk.Button(self, text="Build contour", command=self.build_contour)
        button_build_contour.pack(side=LEFT)

    def build_contour(self):
        pass
