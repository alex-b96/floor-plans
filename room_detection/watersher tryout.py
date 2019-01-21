
import cv2
import numpy as np
import random as rng

# load
from room_detection.build_contour import build_contour

# 18, 39, 40
test_image = 'data/more/plattegrond-18.jpg'
img = cv2.imread(test_image)
cv2.imshow('origin', img)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Build contours
dd = cv2.dilate(gray, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=2)
ee = cv2.erode(dd, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=2)
_, bw = cv2.threshold(ee, 100, 255, cv2.THRESH_BINARY)
cv2.imshow('BW', bw)

thresh = build_contour(img)
cv2.imshow('Contour', thresh)

border = cv2.dilate(img, None, iterations=5)
border = border - cv2.erode(border, None)
cv2.imshow('border', border)

# closing = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7)), iterations=1)
# eroded = cv2.erode(closing, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=2)
# dilated = cv2.dilate(eroded, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=2)
# opening = cv2.morphologyEx(dilated, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=1)
# _, t2 = cv2.threshold(opening, 100, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
# cv2.imshow('trial', t2)
#
# cv2.waitKey(0)

# Find Distance Transformation
dist_transform = cv2.distanceTransform(thresh, cv2.DIST_L2, 5)
cv2.normalize(dist_transform, dist_transform, 0, 1.0, cv2.NORM_MINMAX)
cv2.imshow('Distance Transform', dist_transform)

# Center areas
_, dist = cv2.threshold(dist_transform, 0.4, 1.0, cv2.THRESH_BINARY)
kernel1 = np.ones((3, 3), dtype=np.uint8)
dist = cv2.dilate(dist, kernel1)
cv2.imshow('dist', dist)

# dist = np.uint8(dist)
# _, markers = cv2.connectedComponents(dist)
# markers = markers + 1

# markers = cv2.imread('data/1 copy.jpg')
# markers = cv2.cvtColor(markers, cv2.COLOR_BGR2GRAY)
# markers = cv2.threshold(markers, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

dist_8u = dist.astype('uint8')
_, contours, _ = cv2.findContours(dist_8u, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
print('contours len ', len(contours))
markers = np.zeros(dist.shape, dtype=np.int32)
for i in range(len(contours)):
    cv2.drawContours(markers, contours, i, (i+1), -1)
cv2.circle(markers, (5, 5), 3, (255, 255, 255), -1)
cv2.imshow('Markers', markers*1000)

# markers[thresh == 0] = 0

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
cv2.imshow('Final Result', dst)

cv2.waitKey(0)
