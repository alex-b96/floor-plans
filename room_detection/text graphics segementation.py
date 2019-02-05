
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

img = cv2.imread('data/raw/1.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

dilated = cv2.dilate(gray, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=2)
eroded = cv2.erode(dilated, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)), iterations=2)
_, thresh = cv2.threshold(eroded, 100, 255, cv2.THRESH_BINARY)

difference = cv2.bitwise_not(cv2.bitwise_not(gray) - cv2.bitwise_not(eroded))
_, difference_inv = cv2.threshold(difference, 200, 255, cv2.THRESH_BINARY_INV)

components, connected_components = cv2.connectedComponents(difference_inv)
areas = []
heights, widths = [], []
all_symbols = thresh.copy()
perimeters = []
for i in range(1, components):
    indexes = np.where(connected_components == i)
    x1, x2 = min(indexes[0]), max(indexes[0])
    y1, y2 = min(indexes[1]), max(indexes[1])
    cv2.rectangle(all_symbols, (y1 - 1, x1 - 1), (y2 + 2, x2 + 2), 0, 1)
    area = abs(y1 - y2) * abs(x1 - x2)
    areas.append(area)
    heights.append(abs(y1 - y2))
    widths.append(abs(x1 - x2))
    perimeters.append(2 * abs(y1 - y2) + 2 * abs(x1 - x2))

hist, bin_edges = np.histogram(areas)

a_avg = np.mean(areas)
a_mp = np.mean([ele for ele in areas if bin_edges[hist.argmax()] < ele < bin_edges[hist.argmax() + 1]])

t1 = 5.0 * max(a_mp, a_avg)
t2 = max(np.mean(heights), np.mean(widths))

selected_symbols = thresh.copy()
count = 0
for i in range(1, components):
    indexes = np.where(connected_components == i)
    x1, x2 = min(indexes[0]), max(indexes[0])
    y1, y2 = min(indexes[1]), max(indexes[1])
    area = abs(y1 - y2) * abs(x1 - x2)
    if not x1 == x2:
        if area < t1 and \
                1 / t2 < abs(y1 - y2) / abs(x1 - x2) < t2 and \
                abs(y1 - y2) < np.sqrt(t1) and abs(x1 - x2) < np.sqrt(t1):
            cv2.rectangle(selected_symbols, (y1 - 1, x1 - 1), (y2 + 2, x2 + 2), 0, 1)

for i in range(1, components):
    indexes = np.where(connected_components == i)
    x1, x2 = min(indexes[0]), max(indexes[0])
    y1, y2 = min(indexes[1]), max(indexes[1])
    cv2.rectangle(thresh, (y1 - 1, x1 - 1), (y2 + 2, x2 + 2), 0, 1)


plt.figure(figsize=(16, 8))

gs = gridspec.GridSpec(1, 4)

plt.subplot(gs[0, 0]), plt.imshow(gray, cmap='gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])

plt.subplot(gs[0, 1]), plt.imshow(all_symbols, cmap='gray')
plt.title('All Symbols'), plt.xticks([]), plt.yticks([])

plt.subplot(gs[0, 2]), plt.imshow(selected_symbols, cmap='gray')
plt.title('Selected Symbols'), plt.xticks([]), plt.yticks([])

plt.subplot(gs[0, 3])
plt.hist(perimeters, bins=10)
plt.title('Histogram')

plt.show()

cv2.waitKey(0)
