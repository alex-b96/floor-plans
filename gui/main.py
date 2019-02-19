
from tkinter import *
from tkinter import ttk

from gui.canvas.frameCanvas import FrameCanvas
from gui.controls.controls import Controls


class Window(ttk.Frame):

    def __init__(self):
        super().__init__()

        self.style = None

        self.points_asd = []
        self.points = []
        self.shapes = []

        self.init_window()

    def init_window(self):
        self.master.title("2-measure.it")

        self.style = ttk.Style()
        self.style.theme_use("default")

        FrameCanvas(self).pack(fill=BOTH, side=LEFT)

        controls = Controls(self)
        controls.pack(fill=BOTH, padx=20, pady=20)

        self.pack(fill=BOTH)


root = Tk()

width = 1400
height = 900

# Get screen width and height
width_screen = root.winfo_screenwidth()
height_screen = root.winfo_screenheight()

# Calculate x and y coordinates for the Tk root window
x = (width_screen / 2) - (width / 2)
y = (height_screen / 2) - (height / 2) - 40

# Set the dimensions of the screen and where it is placed
root.geometry('%dx%d+%d+%d' % (width, height, x, y))
root.resizable(False, False)

app = Window()

root.mainloop()
