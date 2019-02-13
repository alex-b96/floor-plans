
import cv2
import numpy as np


img = cv2.imread('data/raw/1.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow('Gray', gray)

dilated = cv2.dilate(gray, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=2)
eroded = cv2.erode(dilated, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=2)
_, thresh = cv2.threshold(eroded, 100, 255, cv2.THRESH_BINARY)
cv2.imshow('th', thresh)

dst = cv2.cornerHarris(gray, 2, 3, 0.04)
dst = cv2.dilate(dst, None)
corners = dst > 0.1 * dst.max()

room_closing_max_length = 100
for y, row in enumerate(corners):
    x_same_y = np.argwhere(row)
    for x1, x2 in zip(x_same_y[:-1], x_same_y[1:]):
        if x2[0] - x1[0] < room_closing_max_length:
            color = 0
            cv2.line(thresh, (x1, y), (x2, y), color, 1)

for x, col in enumerate(corners.T):
    y_same_x = np.argwhere(col)
    for y1, y2 in zip(y_same_x[:-1], y_same_x[1:]):
        if y2[0] - y1[0] < room_closing_max_length:
            color = 0
            cv2.line(thresh, (x, y1), (x, y2), color, 1)
cv2.imshow('th', thresh)

img[dst > 0.01 * dst.max()] = [0, 0, 255]
cv2.imshow('img', img)

cv2.waitKey(0)
