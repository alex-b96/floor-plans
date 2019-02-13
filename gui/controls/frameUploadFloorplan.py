import cv2
from tkinter import ttk, LEFT, filedialog, CENTER

import numpy as np
from PIL import ImageTk, Image

from gui import config
from room_detection.core.buildCorners import BuildCorners


class FrameUploadFloorplan(ttk.Frame):

    def __init__(self, parent):

        super().__init__(parent)

        # Upload floor plan button
        button_upload = ttk.Button(self, text="Upload floor plan", command=self.upload_floor_plan)
        button_upload.pack(side=LEFT)

    @staticmethod
    def upload_floor_plan():
        image_location = filedialog.askopenfilename(title="Select file",
                                                    filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
        config.cv_img = cv2.cvtColor(cv2.imread(image_location), cv2.COLOR_BGR2RGB)
        config.photo = ImageTk.PhotoImage(image=Image.fromarray(config.cv_img))
        config.canvas.create_image(450, 450, image=config.photo, anchor=CENTER)

        height_bias = (900 - config.photo.height()) / 2
        width_bias = (900 - config.photo.width()) / 2

        a = np.where(BuildCorners.build(config.cv_img))
        for i in range(len(a[0])):
            config.corners.append((a[1][i] + width_bias, a[0][i] + height_bias))
