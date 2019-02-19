from tkinter import ttk, X


class FrameUsageInformation(ttk.Frame):

    def __init__(self, parent):

        super().__init__(parent)

        label = ttk.Label(self, text='Bindings')
        label.config(font=('Arial', 16))
        label.pack(padx=5, pady=5, fill=X)

        ttk.Label(self, text='Ctrl L - Hold to visualize the corner snapping points.').pack(padx=5, pady=5, fill=X)
        ttk.Label(self, text='Left Click').pack(padx=5, pady=5, fill=X)
        ttk.Label(self, text=' - First 2 clicks represent the construction of the `Scale`.')\
            .pack(padx=5, pady=5, fill=X)
        ttk.Label(self, text=' - Next clicks represent corners of a `Room`. Will snap to closest corner.')\
            .pack(padx=5, pady=5, fill=X)
        ttk.Label(self, text=' - To enclose a `Room` click to the initial corner.').pack(padx=5, pady=5, fill=X)
        ttk.Label(self, text='Right Click - Free correction of corner point.').pack(padx=5, pady=5, fill=X)
