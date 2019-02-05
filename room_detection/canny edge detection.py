import cv2
import numpy as np

from room_detection.imageResize import image_resize

img = cv2.imread('data/raw/1.jpg')
gray = 255 - cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

eroded = cv2.erode(gray, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=2)
dilated = cv2.dilate(eroded, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=2)
_, thresh = cv2.threshold(dilated, 100, 255, cv2.THRESH_BINARY)

edges = cv2.Canny(thresh, 100, 200)

minLineLength = 100
maxLineGap = 50
lines = cv2.HoughLinesP(edges,1,np.pi/180,15,minLineLength,maxLineGap)
for x in range(0, len(lines)):
    for x1,y1,x2,y2 in lines[x]:
        cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)

cv2.imshow('edges', edges)
cv2.imshow('img', img)

cv2.waitKey(0)
