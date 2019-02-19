from tkinter import ttk, LEFT, CENTER, TOP, X

from PIL import ImageTk, Image

from gui import config as c

from room_detection.core.buildRooms import BuildRooms


class FrameBuildRooms(ttk.Frame):

    def __init__(self, parent):

        super().__init__(parent)

        f1 = ttk.Frame(self)

        ttk.Label(f1, text='No. iterations').pack(pady=5, side=LEFT)
        self.external_walls_iterations = ttk.Entry(f1)
        self.external_walls_iterations.pack(padx=5, pady=5, side=LEFT)
        self.external_walls_iterations.insert(0, "1")

        ttk.Label(f1, text='Kernel size').pack(padx=5, pady=5, side=LEFT)
        self.external_walls_kernel_size = ttk.Entry(f1)
        self.external_walls_kernel_size.pack(padx=5, pady=5, side=LEFT)
        self.external_walls_kernel_size.insert(0, "5")

        f1.pack(fill=X, side=TOP)

        f2 = ttk.Frame(self)

        ttk.Label(f2, text='Threshold').pack(pady=5, side=LEFT)
        self.external_walls_min_th = ttk.Entry(f2)
        self.external_walls_min_th.pack(padx=5, pady=5, side=LEFT)
        self.external_walls_min_th.insert(0, "128")

        self.external_walls_max_th = ttk.Entry(f2)
        self.external_walls_max_th.pack(padx=5, pady=5, side=LEFT)
        self.external_walls_max_th.insert(0, "255")

        f2.pack(fill=X, side=TOP)

        f3 = ttk.Frame(self)

        ttk.Label(f2, text='Count').pack(pady=5, side=LEFT)
        self.external_walls_count = ttk.Entry(f2)
        self.external_walls_count.pack(padx=5, pady=5, side=LEFT)
        self.external_walls_count.insert(0, "100")

        f3.pack(fill=X, side=TOP)

        button_build_contour = ttk.Button(self, text="Build rooms", command=self.build_rooms)
        button_build_contour.pack(side=LEFT)

    def build_rooms(self):
        c.cv_img = BuildRooms.build(c.cv_img, iterations=int(self.external_walls_iterations.get()),
                                    kernel_size=int(self.external_walls_kernel_size.get()),
                                    min_thresh=int(self.external_walls_min_th.get()),
                                    max_thresh=int(self.external_walls_max_th.get()),
                                    count=int(self.external_walls_count.get()))
        c.photo = ImageTk.PhotoImage(image=Image.fromarray(c.cv_img))
        c.canvas.create_image(450, 450, image=c.photo, anchor=CENTER)
