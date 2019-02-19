import cv2
import numpy as np
import random as rng


class BuildRooms:

    def __init__(self):
        pass

    @staticmethod
    def build(img, min_thresh=128, max_thresh=255, kernel_size=5, iterations=1, count=100):

        # negative BW
        img_negative = 255 - cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        (thresh, img_bw) = cv2.threshold(img_negative, min_thresh, max_thresh, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        img_bw = cv2.erode(img_bw, np.ones((kernel_size, kernel_size), np.uint8), iterations=iterations)

        out = cv2.cvtColor(img_bw, cv2.COLOR_GRAY2RGB)

        img_gold = img_bw
        for i in range(count):

            img_new = cv2.morphologyEx(img_bw, cv2.MORPH_CLOSE, np.ones((2 * i + 3, 2 * i + 3), np.uint8))

            img = cv2.subtract(img_new, img_gold)
            img = cv2.erode(img, np.ones((kernel_size, kernel_size), np.uint8), iterations=iterations)

            if img.max() == 255:
                c = (rng.randint(0, 256), rng.randint(0, 256), rng.randint(0, 256))
                out[img[:] == 255] = c

            img_gold = img_new

        return out
