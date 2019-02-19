from tkinter import ttk, X

from gui.controls.frameAutomatedControls import FrameAutomatedControls
from gui.controls.frameSeparator import FrameSeparator
from gui.controls.frameBasicControls import FrameBasicControls
from gui.controls.frameHeader import FrameHeader
from gui.controls.frameUsageInformation import FrameUsageInformation


class Controls(ttk.Frame):

    def __init__(self, parent):

        super().__init__(parent)

        FrameHeader(self).pack(fill=X, pady=15)

        FrameSeparator(self).pack(fill=X, pady=5)

        FrameBasicControls(self).pack(fill=X, pady=15)

        FrameSeparator(self).pack(fill=X, pady=5)

        FrameAutomatedControls(self).pack(fill=X, pady=15)

        FrameSeparator(self).pack(fill=X, pady=5)

        FrameUsageInformation(self).pack(fill=X, pady=5)
