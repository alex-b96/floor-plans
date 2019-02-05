
import cv2
import numpy as np
import random as rng

# load
# from room_detection.build_contour import build_contour
from room_detection.externalWalls import ExternalWalls
from room_detection.imageResize import image_resize

test_image = 'data/raw/plattegrond-1.jpg'
img = cv2.imread(test_image)
cv2.imshow('Original image 1', image_resize(img))
img = ExternalWalls.build(img)
cv2.imshow('Original image', image_resize(img))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

cv2.waitKey(0)

# Build contours
dd = cv2.dilate(gray, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=2)
ee = cv2.erode(dd, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=2)
_, thresh = cv2.threshold(ee, 100, 255, cv2.THRESH_BINARY)
cv2.imshow('BW', image_resize(thresh))

# cv2.waitKey(0)
#
# thresh = build_contour(img)
# cv2.imshow('Contour', image_resize(thresh))

# cv2.waitKey(0)

# Find Distance Transformation
dist_transform = cv2.distanceTransform(thresh, cv2.DIST_L2, 5)
cv2.normalize(dist_transform, dist_transform, 0, 1.0, cv2.NORM_MINMAX)
# cv2.imshow('Distance Transform', dist_transform)

# Center areas
_, dist = cv2.threshold(dist_transform, 0.1, 1.0, cv2.THRESH_BINARY)
kernel1 = np.ones((3, 3), dtype=np.uint8)
dist = cv2.dilate(dist, kernel1)
# cv2.imshow('dist', dist)

dist_8u = dist.astype('uint8')
_, contours, _ = cv2.findContours(dist_8u, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
print('contours len ', len(contours))
markers = np.zeros(dist.shape, dtype=np.int32)
for i in range(len(contours)):
    cv2.drawContours(markers, contours, i, (i+1), -1)
cv2.circle(markers, (5, 5), 3, (255, 255, 255), -1)
# cv2.imshow('Markers', markers*1000)

asd = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
cv2.watershed(asd, markers)
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

# Visualize the final image
cv2.imshow('Final Result', image_resize(dst))

cv2.waitKey(0)
