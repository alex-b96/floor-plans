from tkinter import ttk, Canvas, BOTH, LEFT

import numpy as np

from gui import config as c

from scipy.spatial import distance


class FrameCanvas(ttk.Frame):

    def __init__(self, parent):

        super().__init__(parent)

        c.canvas = Canvas(self, width=900, height=900)
        c.canvas.pack(fill=BOTH, side=LEFT)
        c.canvas.bind('<Button-1>', self.callback_button_1)
        c.canvas.bind('<B3-Motion>', self.callback_b3_motion)
        c.canvas.bind_all('<KeyPress>', self.callback_key_press)
        c.canvas.bind_all('<KeyRelease>', self.callback_key_release)

    def callback_button_1(self, event, s=5):

        if self._measure_scale(event):
            return

        # Enclose polygon if possible
        if not self._enclose_polygon(event):

            # Snap to corner
            cn = self.__closest_node((event.x, event.y), c.corners)

            # Create new junction point in the current polygon
            pt = c.canvas.create_rectangle(cn[0] - s, cn[1] - s, cn[0] + s, cn[1] + s, fill='red')
            cpt = {'id': pt, 'coords': (cn[0], cn[1])}

            # Create new wall to the current polygon
            if len(c.cur_poly['points']) > 0:
                ppt = c.cur_poly['points'][len(c.cur_poly['points']) - 1]
                wall = c.canvas.create_line(cpt['coords'], ppt['coords'], fill='blue', width=3)
                c.cur_poly['walls'].append({'id': wall, 'pt1': cpt['id'], 'pt2': ppt['id']})

            c.cur_poly['points'].append(cpt)

    def _measure_scale(self, event, s=5):

        # First point
        if len(c.scale['points']) == 0:
            cn = self.__closest_node((event.x, event.y), c.corners)
            pt = c.canvas.create_rectangle(cn[0] - s, cn[1] - s, cn[0] + s, cn[1] + s, fill='green')
            c.scale['points'].append({'id': pt, 'coords': cn})
            return True

        # Second point and length
        if len(c.scale['points']) == 1:

            # Create second point
            cn = self.__closest_node((event.x, event.y), c.corners)
            pt = c.canvas.create_rectangle(cn[0] - s, cn[1] - s, cn[0] + s, cn[1] + s, fill='green')
            c.scale['points'].append({'id': pt, 'coords': cn})

            # Build connection line
            pt1 = c.scale['points'][0]['coords']
            pt2 = c.scale['points'][1]['coords']
            wall = c.canvas.create_line(pt1, pt2, fill='green', width=3)
            c.scale['wall'] = {'id': wall}
            return True

        return False

    def _enclose_polygon(self, event, s=5):

        if len(c.cur_poly['points']) > 0:

            # Check if we clicked on the first point
            fpt = c.cur_poly['points'][0]
            if fpt['coords'][0] + 2*s > event.x > fpt['coords'][0] - 2*s and \
                    fpt['coords'][1] + 2*s > event.y > fpt['coords'][1] - 2*s:

                ppt = c.cur_poly['points'][len(c.cur_poly['points']) - 1]

                # Create last wall to enclose the polygon
                wall = c.canvas.create_line(ppt['coords'], fpt['coords'], fill='blue', width=3)
                c.cur_poly['walls'].append({'id': wall, 'pt1': ppt['id'], 'pt2': fpt['id']})

                # Create background polygon
                inter_list = [list(ele['coords']) for ele in c.cur_poly['points']]
                inter_list = [item for sublist in inter_list for item in sublist]
                bg = c.canvas.create_polygon(inter_list, fill='green', stipple='gray25')
                c.cur_poly['background'] = bg

                # Calculate area size
                c.cur_poly['area'] = round(self.__convert_scale(self.__polygon_area(c.cur_poly['points'])), 2)

                # Display room number
                c.canvas.create_text(np.mean([ele['coords'][0] for ele in c.cur_poly['points']]),
                                     np.mean([ele['coords'][1] for ele in c.cur_poly['points']]),
                                     font="Times 24 bold", text=(str(len(c.polys) + 1)))

                # Display area size
                c.canvas.create_text(np.mean([ele['coords'][0] for ele in c.cur_poly['points']]),
                                     np.mean([ele['coords'][1] for ele in c.cur_poly['points']]) + 30,
                                     font="Times 12", text=('Area: ' + str(c.cur_poly['area']) + ' m2'))

                # Add to `polys` and reset
                c.polys.append(c.cur_poly)
                c.cur_poly = {'points': [], 'walls': [], 'background': None, 'area': None}

                return True

        return False

    @staticmethod
    def callback_b3_motion(event, s=5):

        # Find selected point
        for pt in c.cur_poly['points']:
            if pt['coords'][0] + 2 * s > event.x > pt['coords'][0] - 2 * s and \
                    pt['coords'][1] + 2 * s > event.y > pt['coords'][1] - 2 * s:

                # Move point in canvas
                event.widget.coords(pt['id'], event.x - 5, event.y - 5, event.x + 5, event.y + 5)
                pt['coords'] = (event.x, event.y)

                # Move connected walls
                for wall in c.cur_poly['walls']:
                    if wall['pt1'] == pt['id']:
                        for pt2 in c.cur_poly['points']:
                            if pt2['id'] == wall['pt2']:
                                event.widget.coords(wall['id'], pt['coords'][0], pt['coords'][1],
                                                    pt2['coords'][0], pt2['coords'][1])
                    if wall['pt2'] == pt['id']:
                        for pt1 in c.cur_poly['points']:
                            if pt1['id'] == wall['pt1']:
                                event.widget.coords(wall['id'], pt1['coords'][0], pt1['coords'][1],
                                                    pt['coords'][0], pt['coords'][1])

        pass

    @staticmethod
    def callback_key_press(event):
        if event.keycode == 17:
            for corner in c.corners_visual:
                c.canvas.itemconfigure(corner, state='normal')

    @staticmethod
    def callback_key_release(event):
        if event.keycode == 17:
            for corner in c.corners_visual:
                c.canvas.itemconfigure(corner, state='hidden')

    @staticmethod
    def __closest_node(node, nodes):
        if len(nodes) > 0:
            # noinspection PyTypeChecker
            closest_index = distance.cdist([node], nodes).argmin()
            return nodes[closest_index]
        return node

    @staticmethod
    def __polygon_area(points):
        xs = [ele['coords'][0] for ele in points]
        ys = [ele['coords'][1] for ele in points]
        return 0.5 * np.abs(np.dot(xs, np.roll(ys, 1)) - np.dot(ys, np.roll(xs, 1)))

    @staticmethod
    def __convert_scale(area):
        points = c.scale['points']
        p1 = points[0]['coords']
        p2 = points[1]['coords']
        dist = np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

        pixel_scale_length = c.scale_value / dist
        pixel_squared = pixel_scale_length * pixel_scale_length

        return area * pixel_squared
