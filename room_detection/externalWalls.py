import cv2
import numpy as np
import random as rng
from room_detection.imageResize import image_resize


class ExternalWalls:

    def __init__(self, img):
        self.img = img
        pass

    def build(self):

        gray = cv2.cvtColor(self.remove_background(), cv2.COLOR_BGR2GRAY)

        _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

        dilated = cv2.dilate(thresh, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=2)
        eroded = cv2.erode(dilated, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=2)

        dist_transform = cv2.distanceTransform(eroded, cv2.DIST_L2, 5)
        cv2.normalize(dist_transform, dist_transform, 0, 1.0, cv2.NORM_MINMAX)

        _, dist = cv2.threshold(dist_transform, 0.3, 1.0, cv2.THRESH_BINARY)
        kernel1 = np.ones((3, 3), dtype=np.uint8)
        dist = cv2.dilate(dist, kernel1)

        return eroded

    def remove_background(self):

        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)

        _, thresh = cv2.threshold(gray, 230, 255, cv2.THRESH_BINARY_INV)

        img_, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        largest_contour_area = 0
        largest_contour = None
        for cnt in contours:

            if cv2.contourArea(cnt) > largest_contour_area:
                largest_contour_area = cv2.contourArea(cnt)
                largest_contour = cnt

        epsilon = 0.001 * cv2.arcLength(largest_contour, True)
        largest_contour = cv2.approxPolyDP(largest_contour, epsilon, True)

        stencil = np.zeros_like(self.img)
        color = [255, 255, 255]
        cv2.fillPoly(stencil, [largest_contour], color)
        result = cv2.bitwise_and(self.img, stencil)

        return result


if __name__ == '__main__':
    image = cv2.imread('data/raw/plattegrond-1.jpg')
    cv2.imshow('Original Image', image_resize(image))
    externalWalls = ExternalWalls(image).build()
    cv2.imshow('External Walls', image_resize(externalWalls))
    cv2.waitKey(0)
