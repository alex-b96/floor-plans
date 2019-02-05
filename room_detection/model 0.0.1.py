import cv2
import numpy as np

'''
0. Find Background by generating contour and getting the biggest one
1. Threshold + Erode + Dilate to get the Contour
2. Find the Difference between original image and Contour
3. Find ConnectedComponents from Difference
4. Build Look-up algorithm to close Contour gaps from ConnectedComponents
5. Watershed over the updated Contour to find rooms
'''


def remove_background(img, remove_noise=False):
    """
    To find the Background from an image, find the contours in the image and keep the biggest one.
    - convert the image to gray-scale and invert it on a high threshold
    - [optional] remove noise if needed with Erode + Dilate
    - use `findContours` to find the contours in the image
    - find the Largest Area
    - use approxPoly to refine the contour
    - re-build the initial image without the background
    """

    # Convert to gray-scale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Threshold on high values
    _, thresh = cv2.threshold(gray, 230, 255, cv2.THRESH_BINARY_INV)

    # Remove noise if needed
    if remove_noise:
        thresh = cv2.erode(thresh, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=1)
        thresh = cv2.dilate(thresh, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=1)

    # Compute the contours
    img_, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the largest contour area
    largest_contour_area = 0
    largest_contour = None
    for cnt in contours:
        if cv2.contourArea(cnt) > largest_contour_area:
            largest_contour_area = cv2.contourArea(cnt)
            largest_contour = cnt

    # Refine the contour by approximating the polygon
    epsilon = 0.001 * cv2.arcLength(largest_contour, True)
    largest_contour = cv2.approxPolyDP(largest_contour, epsilon, True)

    # Redraw the initial image without the background
    stencil = np.zeros_like(img)
    color = [255, 255, 255]
    cv2.fillPoly(stencil, [largest_contour], color)
    result = cv2.bitwise_and(img, stencil)

    return result


def find_contour(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    dilated = cv2.dilate(gray, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=2)
    eroded = cv2.erode(dilated, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=2)

    _, thresh = cv2.threshold(eroded, 127, 255, cv2.THRESH_BINARY)

    diff = cv2.bitwise_not(cv2.bitwise_not(gray) - cv2.bitwise_not(eroded))
    _, difference_inv = cv2.threshold(diff, 235, 255, cv2.THRESH_BINARY_INV)

    return thresh, difference_inv


def find_connected_components(diff):
    components, connected_components = cv2.connectedComponents(diff, connectivity=4)
    return components, connected_components


def fill_relevant_components(components, connected_components, thresh):
    for i in range(1, components):

        indexes = np.where(connected_components == i)
        x1, x2 = min(indexes[0]), max(indexes[0])
        y1, y2 = min(indexes[1]), max(indexes[1])

        count = 0
        for ii in range(x1 - 2, x2 + 2):
            if thresh[ii, y1 - 2:y2 + 2][0] == 0:
                count += 1
        left = count / (x2 + 4 - x1)

        count = 0
        for ii in range(x1 - 2, x2 + 2):
            if thresh[ii, y1 - 2:y2 + 2][len(thresh[ii, y1 - 2:y2 + 2]) - 1] == 0:
                count += 1
        right = count / (x2 - x1 + 4)

        count = 0
        for jj in range(y1 - 2, y2 + 2):
            if thresh[x1 - 2:x2 + 2, jj][0] == 0:
                count += 1
        top = count / (y2 - y1 + 4)

        count = 0
        for jj in range(y1 - 2, y2 + 2):
            if thresh[x1 - 2:x2 + 2, jj][len(thresh[x1 - 2:x2 + 2, jj]) - 1] == 0:
                count += 1
        bot = count / (y2 - y1 + 4)

        # Horizontal
        if top < 0.25 and bot < 0.25:
            for ii in range(x1 - 1, x2 + 2):
                if thresh[ii, y1 - 1:y2 + 2][0] == 0 and \
                        thresh[ii, y1 - 1:y2 + 2][len(thresh[ii, y1 - 1:y2 + 2]) - 1] == 0:
                    thresh[ii, y1 - 1:y2 + 2] = len(thresh[ii, y1 - 1:y2 + 2]) * [0]

        # Vertical
        if left < 0.25 and right < 0.25:
            for jj in range(y1 - 1, y2 + 2):
                if thresh[x1 - 1:x2 + 2, jj][0] == 0 and \
                        thresh[x1 - 1:x2 + 2, jj][len(thresh[x1 - 1:x2 + 2, jj]) - 1] == 0:
                    thresh[x1 - 1:x2 + 2, jj] = len(thresh[x1 - 1:x2 + 2, jj]) * [0]

    return thresh


def fill_relevant_components_2(components, connected_components, thresh):
    for i in range(1, components):
        indexes = np.where(connected_components == i)
        x1, x2 = min(indexes[0]), max(indexes[0])
        y1, y2 = min(indexes[1]), max(indexes[1])
        cv2.rectangle(thresh, (y1 - 1, x1 - 1), (y2 + 2, x2 + 2), 0, 1)
    return thresh


if __name__ == '__main__':
    image = cv2.imread('data/raw/5.jpg')
    cv2.imshow('Image', image)

    removed_background = remove_background(image)
    cv2.imshow('Removed background', removed_background)

    contour, difference = find_contour(removed_background)
    cv2.imshow('Contour', contour)
    cv2.imshow('Difference', difference)

    comp, conn_comp = find_connected_components(difference)
    f_contour = fill_relevant_components_2(comp, conn_comp, contour)
    cv2.imshow('f_contour', f_contour)

    cv2.waitKey(0)
