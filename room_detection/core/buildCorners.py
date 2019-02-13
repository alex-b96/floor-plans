import cv2


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


if __name__ == '__main__':
    image = cv2.imread('../data/raw/1.jpg')
    print(BuildCorners.build(image))
