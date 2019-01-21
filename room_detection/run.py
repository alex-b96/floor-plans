import os
import cv2
import tqdm

from room_detection.externalWalls import ExternalWalls

if __name__ == '__main__':

    # Create new directory if does not exist for External Walls
    externalWallsPath = 'data/removed background/'
    if not os.path.exists(externalWallsPath):
        os.makedirs(externalWallsPath)

    # Build and save External Walls
    for _, _, images in os.walk('data/raw/'):
        for image in tqdm.tqdm(images):
            img = cv2.imread('data/raw/' + image)
            removedBackground = ExternalWalls(img).remove_background()
            cv2.imwrite(externalWallsPath + image, removedBackground)
        break
