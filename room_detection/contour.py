import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import tqdm

from room_detection.imageResize import image_resize


class Contour:

    def __init__(self):
        pass

    @staticmethod
    def build(img):
        # Convert to gray-scale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Build External Walls
        eroded, thresh = Contour.get_contours(gray)
        # Get the Difference
        difference = Contour.difference(gray, eroded)
        # Connected components
        components, connected_components = cv2.connectedComponents(difference, connectivity=4)
        # Filled Contour
        filled = Contour.fill_relevant_components(components, connected_components, thresh)
        return filled

    @staticmethod
    def get_contours(gray):
        dilated = cv2.dilate(gray, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=2)
        eroded = cv2.erode(dilated, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=2)
        _, thresh = cv2.threshold(eroded, 100, 255, cv2.THRESH_BINARY)
        return eroded, thresh

    @staticmethod
    def difference(gray, eroded, min_thresh=245):
        difference = cv2.bitwise_not(cv2.bitwise_not(gray) - cv2.bitwise_not(eroded))
        _, difference = cv2.threshold(difference, min_thresh, 255, cv2.THRESH_BINARY_INV)
        difference = cv2.dilate(difference, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=1)
        return difference

    @staticmethod
    def get_connected_components(components, connected_components, thresh):
        highlighted_contours = thresh.copy()
        for i in range(1, components):
            indexes = np.where(connected_components == i)
            x1, x2 = min(indexes[0]), max(indexes[0])
            y1, y2 = min(indexes[1]), max(indexes[1])
            cv2.rectangle(highlighted_contours, (y1 - 1, x1 - 1), (y2 + 2, x2 + 2), 0, 1)
        return highlighted_contours

    @staticmethod
    def fill_relevant_components(components, connected_components, thresh):

        for i in range(1, components):

            indexes = np.where(connected_components == i)
            x1, x2 = min(indexes[0]), max(indexes[0])
            y1, y2 = min(indexes[1]), max(indexes[1])

            count = 0
            for ii in range(x1 - 2, x2 + 2):
                if thresh[ii, y1 - 2:y2 + 2][0] == 0:
                    count += 1
            left = count / (x2 + 4 - x1)

            count = 0
            for ii in range(x1 - 2, x2 + 2):
                if thresh[ii, y1 - 2:y2 + 2][len(thresh[ii, y1 - 2:y2 + 2]) - 1] == 0:
                    count += 1
            right = count / (x2 - x1 + 4)

            count = 0
            for jj in range(y1 - 2, y2 + 2):
                if thresh[x1 - 2:x2 + 2, jj][0] == 0:
                    count += 1
            top = count / (y2 - y1 + 4)

            count = 0
            for jj in range(y1 - 2, y2 + 2):
                if thresh[x1 - 2:x2 + 2, jj][len(thresh[x1 - 2:x2 + 2, jj]) - 1] == 0:
                    count += 1
            bot = count / (y2 - y1 + 4)

            # Horizontal
            if top < 0.25 and bot < 0.25:
                for ii in range(x1 - 1, x2 + 2):
                    if thresh[ii, y1 - 1:y2 + 2][0] == 0 and \
                            thresh[ii, y1 - 1:y2 + 2][len(thresh[ii, y1 - 1:y2 + 2]) - 1] == 0:
                        thresh[ii, y1 - 1:y2 + 2] = len(thresh[ii, y1 - 1:y2 + 2]) * [0]

            # Vertical
            if left < 0.25 and right < 0.25:
                for jj in range(y1 - 1, y2 + 2):
                    if thresh[x1 - 1:x2 + 2, jj][0] == 0 and \
                            thresh[x1 - 1:x2 + 2, jj][len(thresh[x1 - 1:x2 + 2, jj]) - 1] == 0:
                        thresh[x1 - 1:x2 + 2, jj] = len(thresh[x1 - 1:x2 + 2, jj]) * [0]

        return thresh


if __name__ == '__main__':

    image = cv2.imread('data/raw/2.jpg')
    image = image_resize(image, width=1000, height=1000)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    eroded_image, thresh_image = Contour.get_contours(gray_image)
    thresh_image_saved = thresh_image.copy()

    for min_thresh in tqdm.tqdm(range(200, 250, 1)):
        difference_image = Contour.difference(gray_image, eroded_image, min_thresh=min_thresh)
        components_image, connected_components_image = cv2.connectedComponents(difference_image, connectivity=8)
        highlighted_image = Contour.get_connected_components(components_image, connected_components_image, thresh_image)
        thresh_image = Contour.fill_relevant_components(components_image, connected_components_image, thresh_image)

    difference_image = Contour.difference(gray_image, eroded_image, min_thresh=251)
    components_image, connected_components_image = cv2.connectedComponents(difference_image, connectivity=8)
    highlighted_image = Contour.get_connected_components(components_image, connected_components_image, thresh_image)
    filled_image = Contour.fill_relevant_components(components_image, connected_components_image, thresh_image)

    plt.figure(figsize=(16, 8))
    gs = gridspec.GridSpec(1, 4)
    plt.subplot(gs[0, 0]), plt.imshow(image, cmap='gray'), plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(gs[0, 1]), plt.imshow(thresh_image_saved, cmap='gray'), plt.title('Threshold'), plt.xticks([]), plt.yticks([])
    plt.subplot(gs[0, 2]), plt.imshow(highlighted_image, cmap='gray'), plt.title('Highlights'), plt.xticks([]), plt.yticks([])
    plt.subplot(gs[0, 3]), plt.imshow(filled_image, cmap='gray'), plt.title('Contour'), plt.xticks([]), plt.yticks([])
    plt.show()
