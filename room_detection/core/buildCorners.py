import cv2
import numpy as np


class BuildCorners:

    def __init__(self):
        pass

    @staticmethod
    def build(img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        dilated = cv2.dilate(gray, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=2)
        eroded = cv2.erode(dilated, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=2)
        _, thresh = cv2.threshold(eroded, 100, 255, cv2.THRESH_BINARY)

        dst = cv2.cornerHarris(gray, 2, 3, 0.04)
        dst = cv2.dilate(dst, None)
        corners = dst > 0.1 * dst.max()
        return corners

    @staticmethod
    def build2(img):

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # find harris corners
        gray = np.float32(gray)
        dst = cv2.cornerHarris(gray, 2, 3, 0.04)
        dst = cv2.dilate(dst, None)
        _, dst = cv2.threshold(dst, 0.01 * dst.max(), 255, 0)
        dst = np.uint8(dst)

        # find centroids
        ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)

        centroids = np.int0(centroids)

        return centroids


if __name__ == '__main__':
    image = cv2.imread('../data/raw/1.jpg')

    corners = BuildCorners.build2(image)

    image[corners[:, 1], corners[:, 0]] = [0, 0, 255]
    cv2.imshow('Corners', image)

    cv2.waitKey(0)
