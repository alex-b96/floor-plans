import struct
import array
import cv2
import numpy as np
from rubik.project_configurator import ProjectConfigurator


def showvec(fn, width=24, height=24, resize=4.0):
    f = open(fn, 'rb')
    HEADERTYP = '<iihh' # img count, img size, min, max

    # read header
    imgcount, imgsize, _, _ = struct.unpack(HEADERTYP, f.read(12))

    for i in range(imgcount):
        img = np.zeros((height, width), np.uint8)

        # read gap byte
        f.read(1)

        data = array.array('h')

        data.fromfile(f, imgsize)

        for r in range(height):
            for c in range(width):
                img[r, c] = data[r * width + c]

        img = cv2.resize(img, (0, 0), fx=resize, fy=resize, interpolation=cv2.INTER_LINEAR)
        cv2.imshow('vec_img', img)
        k = 0xFF & cv2.waitKey(0)
        if k == 27:         # esc to exit
            break


if __name__ == '__main__':
    vec_file = ProjectConfigurator.get_path_from_storage('temp/cropped.vec')
    showvec(vec_file, 70, 70)
