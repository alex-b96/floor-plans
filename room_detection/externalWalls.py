import cv2
import matplotlib.pyplot as plt


class ExternalWalls:

    def __init__(self):
        pass

    @staticmethod
    def build(img):

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

        dilated = cv2.dilate(thresh, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=2)
        eroded = cv2.erode(dilated, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=2)

        return eroded


if __name__ == '__main__':

    image = cv2.imread('data/raw/17.jpg')
    external_walls = ExternalWalls.build(image)

    plt.figure(figsize=(16, 8))
    plt.subplot(121), plt.imshow(image, cmap='gray')
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(122), plt.imshow(external_walls, cmap='gray')
    plt.title('External Walls'), plt.xticks([]), plt.yticks([])

    plt.show()
