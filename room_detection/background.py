import cv2
import numpy as np
import random as rng


test_image = 'data/more/plattegrond-1.jpg'
img = cv2.imread(test_image)
g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# cv2.imshow('img', img)

# Build contours
g = cv2.dilate(g, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=2)
g = cv2.erode(g, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=2)
_, thresh = cv2.threshold(g, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
cv2.imshow('Contour', thresh)

# Find Distance Transformation
dist_transform = cv2.distanceTransform(thresh, cv2.DIST_L2, 5)
cv2.normalize(dist_transform, dist_transform, 0, 1.0, cv2.NORM_MINMAX)
# cv2.imshow('Distance Transform', dist_transform)

# Center areas
_, dist = cv2.threshold(dist_transform, 0.2, 1.0, cv2.THRESH_BINARY)
dist = cv2.dilate(dist, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)))
cv2.imshow('dist', dist)

dist_8u = dist.astype('uint8')
_, contours, _ = cv2.findContours(dist_8u, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
markers = np.zeros(dist.shape, dtype=np.int32)
for i in range(len(contours)):
    cv2.drawContours(markers, contours, i, (i+1), -1)
cv2.circle(markers, (5, 5), 3, (255,255,255), -1)
cv2.imshow('Markers', markers*10000)

asd = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
cv2.watershed(asd, markers)
mark = markers.astype('uint8')
mark = cv2.bitwise_not(mark)
colors = []
for contour in contours:
    colors.append((rng.randint(0,256), rng.randint(0,256), rng.randint(0,256)))
# Create the result image
dst = np.zeros((markers.shape[0], markers.shape[1], 3), dtype=np.uint8)
# Fill labeled objects with random colors
for i in range(markers.shape[0]):
    for j in range(markers.shape[1]):
        index = markers[i,j]
        if index > 0 and index <= len(contours):
            dst[i,j,:] = colors[index-1]

# Visualize the final image
cv2.imshow('Final Result', dst)

cv2.waitKey(0)
