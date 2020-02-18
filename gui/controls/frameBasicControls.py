import cv2
from tkinter import ttk, LEFT, filedialog, CENTER, StringVar, TOP, X, RIGHT

import numpy as np
from PIL import ImageTk, Image

from gui import config as c
from room_detection.core.buildCorners import BuildCorners
from room_detection.imageResize import image_resize


class FrameBasicControls(ttk.Frame):

    def __init__(self, parent):

        super().__init__(parent)

        frame1 = ttk.Frame(self)

        label = ttk.Label(frame1, text='Basic Controls')
        label.config(font=('Arial', 16))
        label.pack(padx=5, pady=5, side=LEFT)

        frame1.pack(fill=X, side=TOP, pady=10)

        frame2 = ttk.Frame(self)

        # Upload floor plan button
        button_upload = ttk.Button(frame2, text="Upload floor plan", command=self.upload_floor_plan)
        button_upload.pack(side=LEFT)

        # Text field input for scale value
        f = ttk.Frame(frame2)
        string_var = StringVar()
        string_var.trace("w", lambda name, index, mode, sv=string_var: self.callback(sv))
        ttk.Label(f, text='Scale value (in metres)').pack(padx=5, pady=5, side=LEFT)
        self.entry_scale_value = ttk.Entry(f, textvariable=string_var)
        self.entry_scale_value.pack(padx=5, pady=5, side=LEFT)
        f.pack(fill=X, side=LEFT)

        # Reset all
        button_upload = ttk.Button(frame2, text="Reset all", command=self.reset_everything)
        button_upload.pack(side=RIGHT)

        frame2.pack(fill=X, side=TOP, padx=5)

    @staticmethod
    def upload_floor_plan():
        image_location = filedialog.askopenfilename(title="Select file",
                                                    filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
        # c.cv_img = image_resize(cv2.cvtColor(cv2.imread(image_location), cv2.COLOR_BGR2RGB), width=1500)
        c.cv_img = image_resize(cv2.cvtColor(cv2.imread(image_location), cv2.COLOR_BGR2RGB), size=900)
        c.photo = ImageTk.PhotoImage(image=Image.fromarray(c.cv_img))
        c.canvas.create_image(450, 450, image=c.photo, anchor=CENTER)
        # c.canvas.create_image(750, 550, image=c.photo, anchor=CENTER)

        height_bias = (900 - c.photo.height()) / 2
        width_bias = (900 - c.photo.width()) / 2

        # height_bias = (1100 - c.photo.height()) / 2
        # width_bias = (1300 - c.photo.width()) / 2

        _, corners = BuildCorners.build(c.cv_img)
        a = np.where(corners)
        for i in range(len(a[0])):
            c.corners.append((a[1][i] + width_bias, a[0][i] + height_bias))

        for cn in c.corners:
            rect = c.canvas.create_rectangle(cn[0] - 1, cn[1] - 1, cn[0] + 1, cn[1] + 1,
                                             fill='blue', state='hidden', outline='')
            c.corners_visual.append(rect)

    def callback(self, _):
        try:
            c.scale_value = float(self.entry_scale_value.get())
        except ValueError:
            pass

    @staticmethod
    def reset_everything():

        c.canvas.delete('all')
        c.cv_img = None
        c.photo = None

        c.corners = []
        c.corners_visual = []

        c.scale_value = 0.0

        c.polys = []
        c.cur_poly = {
            'points': [],
            'walls': [],
            'background': None,
            'area': None
        }
        c.scale = {
            'points': [],
            'length': None,
            'wall': {}
        }
