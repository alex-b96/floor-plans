import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

img = cv2.imread('data/raw/1.jpg')
imgNegative = 255 - cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = 255 - cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

eroded = cv2.erode(gray, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=2)
dilated = cv2.dilate(eroded, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=2)
_, thresh = cv2.threshold(dilated, 100, 255, cv2.THRESH_BINARY)

image_, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

for i in range(len(contours)):
    hull = cv2.convexHull(contours[i], False)
    cv2.drawContours(img, [hull], -1, (0, 0, 255), 3)

plt.figure(figsize=(16, 9))
gs = gridspec.GridSpec(1, 2)

plt.subplot(gs[0, 0]), plt.imshow(img, cmap='gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(gs[0, 1]), plt.imshow(thresh, cmap='gray')
plt.title('Threshold'), plt.xticks([]), plt.yticks([])

plt.show()
cv2.waitKey(0)
