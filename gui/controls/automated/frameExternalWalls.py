from tkinter import ttk, CENTER, LEFT, TOP, X
from PIL import ImageTk, Image
from gui import config
from room_detection.core.externalWalls import ExternalWalls


class FrameExternalWalls(ttk.Frame):

    def __init__(self, parent):

        super().__init__(parent)

        f1 = ttk.Frame(self)

        ttk.Label(f1, text='No. iterations').pack(pady=5, side=LEFT)
        self.external_walls_iterations = ttk.Entry(f1)
        self.external_walls_iterations.pack(padx=5, pady=5, side=LEFT)
        self.external_walls_iterations.insert(0, "2")

        ttk.Label(f1, text='Kernel size').pack(padx=5, pady=5, side=LEFT)
        self.external_walls_kernel_size = ttk.Entry(f1)
        self.external_walls_kernel_size.pack(padx=5, pady=5, side=LEFT)
        self.external_walls_kernel_size.insert(0, "3")

        f1.pack(fill=X, side=TOP)

        f2 = ttk.Frame(self)

        ttk.Label(f2, text='Threshold').pack(pady=5, side=LEFT)
        self.external_walls_min_th = ttk.Entry(f2)
        self.external_walls_min_th.pack(padx=5, pady=5, side=LEFT)
        self.external_walls_min_th.insert(0, "127")

        self.external_walls_max_th = ttk.Entry(f2)
        self.external_walls_max_th.pack(padx=5, pady=5, side=LEFT)
        self.external_walls_max_th.insert(0, "255")

        f2.pack(fill=X, side=TOP)

        f3 = ttk.Frame(self)

        self.button_external_walls = ttk.Button(f3, text="Get External Walls", command=self.ext_walls)
        self.button_external_walls.pack(pady=5, side=LEFT)

        f3.pack(fill=X, side=TOP)

    def ext_walls(self):
        config.cv_img = ExternalWalls.build(config.cv_img, iterations=int(self.external_walls_iterations.get()),
                                            kernel_size=(int(self.external_walls_kernel_size.get()),
                                                         int(self.external_walls_kernel_size.get())),
                                            threshold_min=int(self.external_walls_min_th.get()),
                                            threshold_max=int(self.external_walls_max_th.get()))
        config.photo = ImageTk.PhotoImage(image=Image.fromarray(config.cv_img))
        config.canvas.create_image(450, 450, image=config.photo, anchor=CENTER)
