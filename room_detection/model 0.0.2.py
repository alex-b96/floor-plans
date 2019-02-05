
import cv2
import numpy as np
import random as rng

from room_detection.contour import Contour
from room_detection.core.removeBackground import RemoveBackground
from room_detection.externalWalls import ExternalWalls


# Load image
img = cv2.imread('data/raw/3.jpg')

# Remove background
removedBackground = RemoveBackground.build(img)
cv2.imshow("Removed background", removedBackground)

externalWalls = Contour.build(removedBackground)
cv2.imshow('Contour', externalWalls)

# Extract walls
# externalWalls = ExternalWalls.build(removedBackground)
# cv2.imshow('External walls', externalWalls)

dist = cv2.distanceTransform(externalWalls, cv2.DIST_L2, 5)
cv2.normalize(dist, dist, 0, 1.0, cv2.NORM_MINMAX)
cv2.imshow('Distance Transform Image', dist)

_, dist = cv2.threshold(dist, 0.4, 1.0, cv2.THRESH_BINARY)
dist = cv2.dilate(dist, cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5)), iterations=5)
cv2.imshow('Distance Transform Image', dist)


dist_8u = dist.astype('uint8')
_, contours, _ = cv2.findContours(dist_8u, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
print('contours len ', len(contours))
markers = np.zeros(dist.shape, dtype=np.int32)
for i in range(len(contours)):
    cv2.drawContours(markers, contours, i, (i+1), -1)
cv2.circle(markers, (5, 5), 3, (255, 255, 255), -1)

cv2.imshow('markers', markers)

cv2.watershed(removedBackground, markers)
mark = markers.astype('uint8')
mark = cv2.bitwise_not(mark)
colors = []
for contour in contours:
    colors.append((rng.randint(0, 256), rng.randint(0, 256), rng.randint(0, 256)))
# Create the result image
dst = np.zeros((markers.shape[0], markers.shape[1], 3), dtype=np.uint8)
# Fill labeled objects with random colors
for i in range(markers.shape[0]):
    for j in range(markers.shape[1]):
        index = markers[i, j]
        if 0 < index <= len(contours):
            dst[i, j, :] = colors[index-1]
cv2.imshow('dst', dst)

cv2.waitKey(0)
