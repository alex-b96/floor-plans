import cv2
import numpy as np
import random as rng

from room_detection.imageResize import image_resize

img = cv2.imread("data/raw/1.jpg")
img = image_resize(img, width=500, height=500)
cv2.imshow('original', img)

# negative BW
imgNegative = 255 - cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
(thresh, imgbw) = cv2.threshold(imgNegative, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
# cv2.imshow('imgbw in', imgbw)

# clean (erode 5x5)
imgbw = cv2.erode(imgbw, np.ones((5, 5), np.uint8), iterations=1)
# cv2.imshow('erode', imgbw)

# init output
out = cv2.cvtColor(imgbw, cv2.COLOR_GRAY2RGB)

# For kernel from 3 to 203 connect white regions (closing morphological transform), 
# calculate difference from prev step, and clean (erode 5x5; with side effect: borders, not more flat output).
# if anything new print to output
imgold = imgbw
for i in range(100):

    imgnew = cv2.morphologyEx(imgbw, cv2.MORPH_CLOSE, np.ones((2*i+3, 2*i+3), np.uint8))
    
    img = cv2.subtract(imgnew, imgold)
    img = cv2.erode(img, np.ones((5, 5), np.uint8), iterations=1)
    
    if img.max() == 255:
        c = (rng.randint(0, 256), rng.randint(0, 256), rng.randint(0, 256))
        out[img[:] == 255] = c
    
    imgold = imgnew
    

cv2.imshow("out", out)
cv2.waitKey(0)
cv2.destroyAllWindows()
