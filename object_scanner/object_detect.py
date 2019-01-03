import numpy as np
import cv2


#this is the cascade we just made. Call what you want
object_cascade = cv2.CascadeClassifier('.\door_clasif\cascade.xml')

img = cv2.imread('1530D.01.11-181109-Plattegrond begane grond nieuw_0.jpg')


# img = cv2.resize(img, (70,70))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Convert image to binary
binary_img = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)[1]

object = object_cascade.detectMultiScale(binary_img, 1.3, minNeighbors=30, minSize=(100,100), maxSize=(200, 200))

print(object)
for (ex,ey,ew,eh) in object:
    cv2.rectangle(img, (ex, ey), (ex + ew, ey + eh), (0, 0, 255), 2)

cv2.imwrite('binary.jpg', binary_img)
cv2.imwrite('lala.jpg', img)
# cv2.imshow('asd', gray)
# cv2.waitKey(0)
# while 1:
#     ret, img = cap.read()
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     # add this
#     # image, reject levels level weights.
#     object = object_cascade.detectMultiScale(gray, 50, 50)
#
#     # add this
#     for (x,y,w,h) in object:
#         cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),2)
#
#     cv2.imshow('img',img)
#     k = cv2.waitKey(30) & 0xff
#     if k == 27:
#         break
#
# cap.release()
cv2.destroyAllWindows()