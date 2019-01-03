import cv2
import numpy as np
import glob
import ntpath

def resize(input_dir, output_dir, resize_w, resize_h, border_w, border_h):
    for file in glob.glob(input_dir + '/*.png'):
        img = cv2.imread(file, 0)
        resized = cv2.resize(img, (resize_w, resize_h))
        filename = ntpath.basename(file)
        # cv2.imwrite(output_dir + '/' + filename, resized)

        im_w = resize_w + 2 * border_w + 2
        im_h = resize_h + 2 * border_h + 2

        out_im = np.ones((im_w, im_h), np.uint8) * 255
        out_im[border_h:border_h+resize_h,border_w:border_w+resize_w] = resized

        out_binary_img = cv2.threshold(out_im, 254, 255, cv2.THRESH_BINARY)[1]

        cv2.imwrite(output_dir + '/' + filename, out_binary_img)
        # cv2.imshow('asd', out_im)
        # cv2.waitKey(0)

if __name__ == '__main__':
    resize_w = 70
    resize_h = 70

    border_w = 0
    border_h = 0

    resize('c:\data\pycharm\ArhitectureScanner\sample\positives\door_type1/', 'sample/resized_positives', resize_w, resize_h, border_w, border_h)
    # resize('c:\data\pycharm\ArhitectureScanner\sample\\negative_test1', 'sample/resized_negatives', resize_w, resize_h, border_w, border_h)
