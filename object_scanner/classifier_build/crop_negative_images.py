import cv2
import time
import glob
import logging
import pathlib
import shutil
from random import randint
from rubik.project_configurator import ProjectConfigurator
from rubik.external_storage import ExternalStorage

def main():
    """
        Use this method in order to crop negative images in order to train classifier
    """
    img_w = 100
    img_h = 100
    acceptance_ratio = 0.97

    input_imgs = []
    input_dir = ProjectConfigurator.get_path_from_storage('build_classifier/door/negative_images_for_crop', create=True) + '/'
    output_dir = ProjectConfigurator.get_path_from_storage('build_classifier/door/sample_negative_images') + '/'
    images = 2000

    # remove directory
    shutil.rmtree(output_dir)
    pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)

    # read images from input_dir
    for img_filename in glob.glob(input_dir + '/*.jpg'):
        # read image into grayscale
        cv2_img = cv2.imread(img_filename, 0)
        input_imgs.append(cv2_img)

    for img_filename in glob.glob(input_dir + '/*.png'):
        # read image into grayscale
        cv2_img = cv2.imread(img_filename, 0)
        input_imgs.append(cv2_img)

    img_index = 0
    while img_index < images:
        # randomly select image from input_imgs
        image_index = randint(0, len(input_imgs) - 1)
        image = input_imgs[image_index]
        height, width = image.shape

        print('Image index', img_index, 'from', images, 'images -> ', image_index)
        img_x = randint(0, width - img_w)
        img_y = randint(0, height - img_h)

        crop_img = image[img_y:img_y + img_h, img_x:img_x + img_w]
        out_binary_img = cv2.threshold(crop_img, 100, 255, cv2.THRESH_BINARY)[1]
        # struct = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        # struct1 = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        # out_binary_img =~cv2.dilate(~out_binary_img, struct1, anchor=(-1, -1), iterations=1)
        # out_binary_img =~cv2.erode(~out_binary_img, struct, anchor=(-1, -1), iterations=1)

        # Count black/white pixels
        white_pixels, black_pixels = 0, 0
        for line in out_binary_img:
            white_pixels += len(list(filter(lambda pixel: pixel == 255, line)))
            black_pixels += len(list(filter(lambda pixel: pixel == 0, line)))

        print('Black pixels: ', black_pixels)
        print('White pixels: ', white_pixels)

        images_pixels = int(img_w * img_h * acceptance_ratio)

        if white_pixels > images_pixels or black_pixels > images_pixels:
            print('Could not use the image')
            continue

        cv2.imwrite(output_dir + 'negative_' + str(time.time()).replace('.', ',') + '.png', out_binary_img)
        img_index += 1

        # display image
        # cv2.imshow('sad', out_binary_img)
        # cv2.waitKey(1)

    nas2 = ExternalStorage('nas2')

    # Remove existing images from storage
    if not nas2.remove_from_remote('build_classifier/door/sample_negative_images'):
        print('Cannot remove directory from remote location')
        return

    # Upload negative images to remote storage
    if not nas2.upload('build_classifier/door/sample_negative_images'):
        print('Cannot upload images to remote location')
        return


if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)
    main()
