import cv2
import numpy as np


class WallScanner:
    """
        WallScanner object implementation - used to detect walls
    """
    def __init__(self):
        # initialize resulting
        self.__wall = []

    def scan(self, image):
        """
            Scan a given image for walls
            @param image:   image as numpy array (opencv mode)
            @return:        True if image successfully scanned or False otherwise
        """
        self.__wall = []
        # preprocess image
        # gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # binary_img = cv2.threshold(gray_img, 254, 255, cv2.THRESH_BINARY)[1]

        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower_blue = np.array([0, 30, 35])
        upper_blue = np.array([255, 255, 255])
        mask = ~cv2.inRange(hsv, lower_blue, upper_blue)
        struct = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        dilated = cv2.dilate(~mask, struct, anchor=(-1, -1), iterations=1)

        self.__wall = cv2.findContours(dilated.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[1]

        # cv2.imshow('mask', resized_img)
        # cv2.waitKey(0)
        return True

    def __len__(self):
        """
            Get len of detected walls
            @return: len
        """
        return len(self.__wall)

    def __getitem__(self, key):
        """
            Get wall specified by given key
            @param key: -   index of wall
            @return:    -   list of points
        """
        return self.__wall[key]


if __name__ == '__main__':
    ds = WallScanner()
