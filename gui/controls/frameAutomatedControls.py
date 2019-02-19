from tkinter import ttk, X

from gui.controls.automated.frameBuildContour import FrameBuildContour
from gui.controls.automated.frameBuildRooms import FrameBuildRooms
from gui.controls.automated.frameExternalWalls import FrameExternalWalls
from gui.controls.automated.frameRemoveBackground import FrameRemoveBackground


class FrameAutomatedControls(ttk.Frame):

    def __init__(self, parent):

        super().__init__(parent)

        label = ttk.Label(self, text='Automated Controls')
        label.config(font=('Arial', 16))
        label.pack(padx=5, pady=5, fill=X)

        label = ttk.Label(self, text='Remove the background from the current Floor Plan image')
        label.config(font=('Arial', 11))
        label.pack(padx=5, pady=5, fill=X)

        FrameRemoveBackground(self).pack(fill=X, pady=10, padx=5)

        label = ttk.Label(self, text='Detect the walls from the Floor Plan image')
        label.config(font=('Arial', 11))
        label.pack(padx=5, pady=5, fill=X)

        FrameExternalWalls(self).pack(fill=X, pady=10, padx=5)

        label = ttk.Label(self, text='Build Rooms')
        label.config(font=('Arial', 11))
        label.pack(padx=5, pady=5, fill=X)

        FrameBuildRooms(self).pack(fill=X, pady=10, padx=5)
