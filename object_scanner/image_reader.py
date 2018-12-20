import pathlib
import cv2
import os
import numpy as np
from pdf2image import convert_from_path


class ImageReader:
    """
        This object is used in order to read images or pdf images and to offer an easy to use
        interface in order to obtain images
    """
    def __init__(self):
        self.__images = []

    def read(self, path_to_file):
        """
            Read images from give path (could be pdf or another image extension supported by opencv)
            If a pdf path was given then the pdf content will be converted into image

            @param path_to_file:    valid path from disk
            @return: True if given path was successfully read or false otherwise
        """
        print('Trying to read image from path', path_to_file)
        self.__images = []

        if path_to_file is None or path_to_file == '':
            print('Given file path is empty or none')
            return False

        if not os.path.exists(path_to_file) or not os.path.isfile(path_to_file):
            print('Given file', path_to_file, 'does not exist or is not a regular file')
            return False

        file_extension = pathlib.PurePosixPath(path_to_file).suffix
        if file_extension == '.pdf' or file_extension == '.PDF':
            print('Read pdf file')
            pil_imgs = convert_from_path(path_to_file)

            for pil_img in pil_imgs:
                cv2_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
                print(cv2_img.shape)
                self.__images.append(cv2_img)
        else:
            print('Read image file')
            self.__images.append(cv2.imread(path_to_file))

        return True

    def __len__(self):
        """
            Get len of stored images
            @return:    len
        """
        return len(self.__images)

    def __getitem__(self, key):
        """
            Get item given by the key
            @param key:  should be a value between 0, len(object)
            @return:     image as numpy array converted into opencv image
        """
        return self.__images[key]


if __name__ == '__main__':
    ir = ImageReader()
    ir.read('d:\Workspace\\tmp\\1530D.01.12-181109-Plattegrond eerst verdieping nieuw.pdf')

    print(ir[0])