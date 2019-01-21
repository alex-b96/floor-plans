import cv2
import pytesseract
import tesseract

img = cv2.imread('data/more/plattegrond-18.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
print(pytesseract.image_to_string(img))
