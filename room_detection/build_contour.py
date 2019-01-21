import cv2
import numpy as np
import sys

from room_detection.imageResize import image_resize

np.set_printoptions(threshold=np.nan)


def build_contour(img):

    # Convert to gray-scale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Get contours
    dilated = cv2.dilate(gray, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=2)
    eroded = cv2.erode(dilated, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=2)
    _, thresh = cv2.threshold(eroded, 100, 255, cv2.THRESH_BINARY)
    cv2.imshow('bw', image_resize(thresh))

    difference = cv2.bitwise_not(cv2.bitwise_not(gray) - cv2.bitwise_not(eroded))
    _, difference = cv2.threshold(difference, 200, 255, cv2.THRESH_BINARY_INV)
    difference = cv2.dilate(difference, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=1)
    # cv2.imshow('Difference', image_resize(difference))

    # Connected components
    elements = []
    areas = []
    components, connected_components = cv2.connectedComponents(difference, connectivity=4)
    for i in range(1, components):
        # if i == 14:
            indexes = np.where(connected_components == i)
            x1, x2 = min(indexes[0]), max(indexes[0])
            y1, y2 = min(indexes[1]), max(indexes[1])

            # print(thresh[x1-1:x2+2, y1-1:y2+2])

            # cv2.rectangle(thresh, (y1-1, x1-1), (y2+2, x2+2), 0, 1)

            count = 0
            for ii in range(x1-2, x2+2):
                if thresh[ii, y1-2:y2+2][0] == 0:
                    count += 1
            left = count / (x2 + 4 - x1)

            count = 0
            for ii in range(x1 - 2, x2 + 2):
                if thresh[ii, y1-2:y2+2][len(thresh[ii, y1-2:y2+2]) - 1] == 0:
                    count += 1
            right = count / (x2 - x1 + 4)

            count = 0
            for jj in range(y1 - 2, y2 + 2):
                if thresh[x1 - 2:x2 + 2, jj][0] == 0:
                    count += 1
            top = count / (y2 - y1 + 4)

            count = 0
            for jj in range(y1 - 2, y2 + 2):
                if thresh[x1-2:x2+2, jj][len(thresh[x1-2:x2+2, jj]) - 1] == 0:
                    count += 1
            bot = count / (y2 - y1 + 4)

            # print(top, right, bot, left)

            # Horizontal
            if top < 0.25 and bot < 0.25:
                for ii in range(x1-1, x2+2):
                    if thresh[ii, y1-1:y2+2][0] == 0 and thresh[ii, y1-1:y2+2][len(thresh[ii, y1-1:y2+2]) - 1] == 0:
                        thresh[ii, y1-1:y2+2] = len(thresh[ii, y1-1:y2+2]) * [0]

            # Vertical
            if left < 0.25 and right < 0.25:
                for jj in range(y1-1, y2+2):
                    if thresh[x1-1:x2+2, jj][0] == 0 and thresh[x1-1:x2+2, jj][len(thresh[x1-1:x2+2, jj]) - 1] == 0:
                        thresh[x1 - 1:x2 + 2, jj] = len(thresh[x1-1:x2+2, jj]) * [0]

    return thresh


if __name__ == '__main__':

    test_image = 'data/raw/plattegrond-4.jpg'
    img = cv2.imread(test_image)
    cv2.imshow('Source', image_resize(img, height=800))

    contour = build_contour(img)
    cv2.imshow('Contour', image_resize(contour, height=800))

    cv2.waitKey(0)
