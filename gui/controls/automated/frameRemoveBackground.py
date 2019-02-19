from tkinter import ttk, CENTER, LEFT

from PIL import ImageTk, Image

from gui import config
from room_detection.core.removeBackground import RemoveBackground


class FrameRemoveBackground(ttk.Frame):

    def __init__(self, parent):

        super().__init__(parent)

        button_remove_background = ttk.Button(self, text="Remove background", command=self.rm_bg)
        button_remove_background.pack(side=LEFT)

    @staticmethod
    def rm_bg():
        config.cv_img = RemoveBackground.build(config.cv_img)
        config.photo = ImageTk.PhotoImage(image=Image.fromarray(config.cv_img))
        config.canvas.create_image(450, 450, image=config.photo, anchor=CENTER)
