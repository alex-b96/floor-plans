import cv2
import random
img = cv2.imread('data/2.jpg')

gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

_, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

cv2.imshow("thresh", thresh)

mor_img = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, (5, 5), iterations=3)

_, contours, _ = cv2.findContours(mor_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)

for c in sorted_contours[1:]:
    area = cv2.contourArea(c)
    if area > 10000:
        cv2.drawContours(img, [c], -1, (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)), 3)

cv2.imshow("img", img)

cv2.waitKey(0)
