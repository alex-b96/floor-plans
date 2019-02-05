import cv2
import numpy as np
import matplotlib.pyplot as plt


class RemoveBackground:

    def __init__(self):
        pass

    @staticmethod
    def build(img, remove_noise=False):

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        _, thresh = cv2.threshold(gray, 230, 255, cv2.THRESH_BINARY_INV)

        if remove_noise:
            thresh = cv2.erode(thresh, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=1)
            thresh = cv2.dilate(thresh, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=1)

        img_, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        largest_contour_area = 0
        largest_contour = None
        for cnt in contours:

            if cv2.contourArea(cnt) > largest_contour_area:
                largest_contour_area = cv2.contourArea(cnt)
                largest_contour = cnt

        epsilon = 0.001 * cv2.arcLength(largest_contour, True)
        largest_contour = cv2.approxPolyDP(largest_contour, epsilon, True)

        stencil = np.zeros_like(img)
        color = [255, 255, 255]
        cv2.fillPoly(stencil, [largest_contour], color)
        result = cv2.bitwise_and(img, stencil)

        return result


if __name__ == '__main__':

    image = cv2.imread('../data/1.jpg')
    removed_background = RemoveBackground.build(image)

    plt.figure(figsize=(16, 8))
    plt.subplot(121), plt.imshow(image, cmap='gray')
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(122), plt.imshow(removed_background, cmap='gray')
    plt.title('Removed Background'), plt.xticks([]), plt.yticks([])

    plt.show()
