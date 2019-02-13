import cv2

import numpy as np

from tkinter import *
from tkinter import ttk

from gui import config
from gui.controls.controls import Controls

from scipy.spatial import distance


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

        config.canvas = Canvas(self, width=900, height=900)
        config.canvas.pack(fill=BOTH, side=LEFT)
        config.canvas.bind('<Button-1>', self.callback_left_click)
        config.canvas.bind('<B3-Motion>', self.callback_right_click)

        controls = Controls(self)
        controls.pack(fill=BOTH, side=TOP, padx=20, pady=20)

        self.pack(fill=BOTH)

    def callback_left_click(self, event, s=5):

        filled_shape = False

        def closest_node_2(node, nodes):
            closest_index = distance.cdist([node], nodes).argmin()
            return nodes[closest_index]

        # Enclose polygon if possible
        if len(self.points) > 0:
            first_point = self.points[0]
            if first_point['x'] + 2*s > event.x > first_point['x'] - 2*s and \
                    first_point['y'] + 2*s > event.y > first_point['y'] - 2*s:

                prev_point = self.points[len(self.points) - 1]
                config.canvas.create_line(prev_point['x'], prev_point['y'], first_point['x'], first_point['y'],
                                          fill='blue', width=3)
                filled_shape = True
                inter_list = [list(ele.values()) for ele in self.points]
                inter_list = [item for sublist in inter_list for item in sublist]
                config.canvas.create_polygon(inter_list, fill='green', stipple="gray25")

                def polygon_area(points):
                    xs = [ele['x'] for ele in points]
                    ys = [ele['y'] for ele in points]
                    return 0.5 * np.abs(np.dot(xs, np.roll(ys, 1)) - np.dot(ys, np.roll(xs, 1)))

                config.canvas.create_text(np.mean([ele['x'] for ele in self.points]),
                                          np.mean([ele['y'] for ele in self.points]),
                                          font="Times 24 bold",
                                          text=(str(len(self.shapes) + 1)))

                config.canvas.create_text(np.mean([ele['x'] for ele in self.points]),
                                          np.mean([ele['y'] for ele in self.points]) + 30,
                                          font="Times 12",
                                          text=('Area: ' + str(polygon_area(self.points)) + ' m2'))

                self.shapes.append({'points': self.points, 'polygon_area': polygon_area(self.points)})
                self.points = []

        if not filled_shape:
            point = (event.x, event.y)
            if len(config.corners) > 0:
                point = closest_node_2((event.x, event.y), config.corners)
            config.canvas.create_rectangle(point[0] - s, point[1] - s, point[0] + s, point[1] + s, fill='red',
                                           tags=('pt' + str(len(self.points))))
            if len(self.points) > 0:
                prev_point = self.points[len(self.points) - 1]
                config.canvas.create_line(point[0], point[1], prev_point['x'], prev_point['y'], fill='blue', width=3)
            self.points.append({'x': point[0], 'y': point[1]})

    def callback_right_click(self, event, s=5):
        for point in self.points:
            if point['x'] + 2 * s > event.x > point['x'] - 2 * s and point['y'] + 2 * s > event.y > point['y'] - 2 * s:
                config.canvas.move('pt0', event.x, event.y)
                print(event.x, event.y)


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

app = Window()

root.mainloop()
