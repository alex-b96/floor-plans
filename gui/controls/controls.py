from tkinter import ttk, X

from gui.controls.frameBuildContour import FrameBuildContour
from gui.controls.frameExternalWalls import FrameExternalWalls
from gui.controls.frameRemoveBackground import FrameRemoveBackground
from gui.controls.frameScaleValue import FrameScaleValue
from gui.controls.frameUploadFloorplan import FrameUploadFloorplan


class Controls(ttk.Frame):

    def __init__(self, parent):

        super().__init__(parent)

        FrameScaleValue(self).pack(fill=X, pady=15)

        FrameUploadFloorplan(self).pack(fill=X, pady=15)

        FrameRemoveBackground(self).pack(fill=X, pady=15)

        FrameExternalWalls(self).pack(fill=X, pady=15)

        FrameBuildContour(self).pack(fill=X, pady=15)
