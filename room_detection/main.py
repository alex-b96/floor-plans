
import cv2
import numpy as np


def image_resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation=inter)

    # return the resized image
    return resized


def find_wall(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([0, 30, 35])
    upper_blue = np.array([255, 255, 255])
    mask = ~cv2.inRange(hsv, lower_blue, upper_blue)
    struct = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    dilated = cv2.dilate(~mask, struct, anchor=(-1, -1), iterations=1)
    contour = cv2.findContours(dilated.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[1]
    return contour


test_image = 'data/raw/1.jpg'
img = cv2.imread(test_image)
cv2.imshow('Source', image_resize(img, height=800))

THRESH = 5

# Find edges
ret, thresh1 = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)
kernel = np.ones((THRESH, THRESH), np.uint8)
out = cv2.dilate(thresh1, kernel)
cv2.imshow('Edges', image_resize(out, height=800))

# Now we transform our edges image to a gray-scale and a binary one, respectively:
bw = cv2.cvtColor(out, cv2.COLOR_BGR2GRAY)
_, bw = cv2.threshold(bw, 40, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
cv2.imshow('Binary Image', image_resize(bw, height=800))

cv2.imshow('Binary Image 2', image_resize(bw, height=800))

# Distance Transform
dist = cv2.distanceTransform(bw, cv2.DIST_L2, 5)
cv2.normalize(dist, dist, 0, 1.0, cv2.NORM_MINMAX)
cv2.imshow('Distance Transform Image', image_resize(dist, height=800))

# centerAreas = cv2.dilate(dist, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=3)
# cv2.imshow('Dilated', image_resize(centerAreas, height=800))
# difference = cv2.bitwise_not(cv2.bitwise_not(dist) - cv2.bitwise_not(centerAreas))
# cv2.imshow('Difference', image_resize(difference, height=800))



# Center Areas
# centerAreas = cv2.dilate(dist, cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5)), iterations=15)
# cv2.imshow('Dilated dist', image_resize(centerAreas, height=800))

# wsh = cv2.watershed(cv2.bitwise_not(dist), dilation)
# print(wsh)

# centerAreas = ImageDifference[ (GeodesicDilation[Image[ImageData[distTransform] - 10], distTransform]), distTransform]

# morph = cv2.morphologyEx(dist, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_CROSS, (50, 50)))
# cv2.imshow('Moprh', image_resize(morph, height=800))



# Watershed
# cv2.watershed(dist, markers)
# mark = markers.astype('uint8')
# mark = cv2.bitwise_not(mark)
#
# cv2.imshow('Markers', markers)



# Image difference (GeodesicDilation(img-10,img) , img)

# We extract the peaks from the above image:
# _, th = cv2.threshold(dist, 0.01, 1.0, cv2.THRESH_BINARY)
# cv2.imshow('asd', image_resize(th, height=800))
#
# kernel1 = np.ones((3, 3), dtype=np.uint8)
# dd = cv2.dilate(th, kernel1)
# cv2.imshow('asd2', image_resize(dd, height=800))


# Pretty much I need to apply watershed:


cv2.waitKey(0)


# THRESH = 5
#
# # Read image and convert to Gray Scale
# img = cv2.imread(test_image)
# # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#
# # Thresh method
# ret, thresh1 = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY)
#
# kernel = np.ones((THRESH, THRESH), np.uint8)
# out = cv2.dilate(thresh1, kernel)
# out = cv2.erode(out, cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5), (-1, -1)))
# out = cv2.dilate(out, cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5), (-1, -1)))
#
# cv2.imshow('mask', image_resize(find_wall(img), height=800))
# cv2.waitKey(0)
