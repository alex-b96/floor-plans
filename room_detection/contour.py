import cv2
import matplotlib.pyplot as plt
import numpy as np

# Load image
test_image = 'data/more/plattegrond-1.jpg'
img = cv2.imread(test_image)

# Convert to gray-scale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow('Gray', gray)


# Get contours
dilated = cv2.dilate(gray, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=2)
eroded = cv2.erode(dilated, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=2)
_, thresh = cv2.threshold(eroded, 100, 255, cv2.THRESH_BINARY)
cv2.imshow('Contour', thresh)

h = cv2.bitwise_not(thresh)
kernel = np.ones((50, 1), np.uint8)
h = cv2.dilate(h, kernel, iterations=2)
h = cv2.erode(h, kernel, iterations=2)
kernel = np.ones((1, 50), np.uint8)
h = cv2.dilate(h, kernel, iterations=2)
h = cv2.erode(h, kernel, iterations=2)
cv2.imshow('trying', h)

components, connected_components = cv2.connectedComponents(h, connectivity=8)
h[connected_components == 0] = 125
cv2.imshow('h', h)

# cv2.waitKey(0)

difference = cv2.bitwise_not(cv2.bitwise_not(gray) - cv2.bitwise_not(eroded))
_, difference = cv2.threshold(difference, 200, 255, cv2.THRESH_BINARY_INV)
difference = cv2.dilate(difference, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=1)
cv2.imshow('Difference', difference)

# Connected components
elements = []
areas = []
components, connected_components = cv2.connectedComponents(difference, connectivity=4)
for i in range(1, components):
    indexes = np.where(connected_components == i)
    x1, x2 = min(indexes[0]), max(indexes[0])
    y1, y2 = min(indexes[1]), max(indexes[1])
    should_draw = True
    for j in range(1, components):
        _indexes = np.where(connected_components == j)
        _x1, _x2 = min(_indexes[0]), max(_indexes[0])
        _y1, _y2 = min(_indexes[1]), max(_indexes[1])
        if y1 > _y1 and x1 > _x1 and y2 < _y2 and x2 < _x2:
            should_draw = False
    if should_draw:
        cv2.rectangle(img, (y1, x1), (y2, x2), (0, 0, 255), 3)
        elements.append(((y1, x1), (y2, x2)))
        areas.append(abs(y2 - y1) * abs(x2 - x1))
cv2.imshow('Img', img)

# plt.hist(areas, bins='auto')
# plt.title("Histogram with 'auto' bins")
# plt.show()

# I am confident in this
# ret, thresh1 = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
# kernel = np.ones((5, 5), np.uint8)
# dilated = cv2.dilate(thresh1, kernel)
# cv2.imshow('Contour', thresh1)

cv2.waitKey(0)
