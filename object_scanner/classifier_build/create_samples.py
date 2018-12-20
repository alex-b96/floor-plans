import glob
import random
import cv2
import time
import shutil
import pathlib
import logging
from rubik.project_configurator import ProjectConfigurator
from rubik.external_storage import ExternalStorage


def create_samples(positive_images_p, negative_images_p, output_images_p, output_samples_each_entry, white_threshold):
    """
        Create sample images from a few positive images and many negative images

        @param positive_images_p:           -   positive images directory
        @param negative_images_p:           -   negative images directory
        @param output_images_p:             -   output images directory
        @param output_samples_each_entry:   -   create x sample images
        @param white_threshold:             -   image white threshold
    """
    # remove directory if exists
    shutil.rmtree(output_images_p)
    pathlib.Path(output_images_p).mkdir(parents=True, exist_ok=True)

    positive_images = glob.glob(positive_images_p + '/*.png')
    negative_images = glob.glob(negative_images_p + '/*.png')
    cropped_text = ''

    if len(negative_images) == 0:
        raise ValueError('There are no negative images')

    if len(positive_images) == 0:
        raise ValueError('There are no positive images')

    for positive_image_p in positive_images:
        positive_image = cv2.imread(positive_image_p, 0)
        positive_image_h_o, positive_image_w_o = positive_image.shape
        select_images = min(len(negative_images), output_samples_each_entry)
        for positive_image_count in range(0, select_images):
            negative_image_index = random.randint(0, select_images - 1)
            # read as grayscale
            negative_image_cv = cv2.imread(negative_images[negative_image_index], 0)
            negative_image_h, negative_image_w = negative_image_cv.shape
            resize_ratio = random.uniform(0.5, 1)

            positive_image_resized = cv2.resize(
                positive_image,
                (int(positive_image_h_o * resize_ratio), int(positive_image_w_o * resize_ratio))
            )
            positive_image_h, positive_image_w = positive_image_resized.shape

            print(positive_image_h, positive_image_w)
            if negative_image_h <= positive_image_h or negative_image_w <= positive_image_w:
                raise ValueError('Negative images width/height should be grater than positive images width/height')

            insert_w = random.randint(0, (negative_image_w - positive_image_w) - 1)
            insert_h = random.randint(0, (negative_image_h - positive_image_h) - 1)

            # white pixels from positive_images will be marked as transparent
            out_image = negative_image_cv.copy()

            for pix_i in range(0, positive_image_h - 1):
                for pix_j in range(0, positive_image_w - 1):
                    pix_value = positive_image_resized[pix_i][pix_j]
                    if pix_value <= white_threshold:
                        out_image[insert_h + pix_i, insert_w + pix_j] = pix_value

            save_image_name = str(time.time()).replace('.', '-') + '.png'
            cropped_text = cropped_text + save_image_name + ' 1 ' + str(insert_w) + ' ' + str(insert_h) + ' ' + str(positive_image_h) + ' ' + str(positive_image_w) + '\n'
            cv2.imwrite(output_images_p + '/' + save_image_name, out_image)

    with open(output_images_p + '/cropped.txt', 'w') as f:
        f.write(cropped_text)

    # Upload samples to remote location
    nas2 = ExternalStorage('nas2')

    # Remove existing images from storage
    if not nas2.remove_from_remote('build_classifier/door/samples'):
        print('Cannot remove directory from remote location')
        return

    # Upload negative images to remote storage
    if not nas2.upload('build_classifier/door/samples'):
        print('Cannot upload images to remote location')
        return


if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)

    positive_images_p = ProjectConfigurator.get_path_from_storage('build_classifier/door/sample_positive_images')
    negative_images_p = ProjectConfigurator.get_path_from_storage('build_classifier/door/sample_negative_images')
    out_samples = ProjectConfigurator.get_path_from_storage('build_classifier/door/samples')

    create_samples(positive_images_p, negative_images_p, out_samples, output_samples_each_entry=400, white_threshold=10)

