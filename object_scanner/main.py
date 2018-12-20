import ntpath
import cv2
import logging
from object_scanner.image_reader import ImageReader
from object_scanner.door_scanner import DoorScanner
from object_scanner.wall_scanner import WallScanner
from random import randint
from rubik.project_configurator import ProjectConfigurator
from rubik.external_storage import ExternalStorage


def process():
    # Create temp and build_classifier path in storage if it is not exists
    ProjectConfigurator.get_path_from_storage('/temp', create=True)
    ProjectConfigurator.get_path_from_storage('/build_classifier', create=True)

    samples_path = ProjectConfigurator.get_path_from_storage('samples') + '/'

    file_path = samples_path + 'pdf/1530D.01.13-181109-Plattegrond tweede verdieping nieuw.pdf'
    out_path = str(ntpath.basename(file_path).rpartition(".")[0])
    print(out_path)

    image_reader = ImageReader()

    if not image_reader.read(file_path):
        print('Cannot read images from given path')
        return False

    if len(image_reader) == 0:
        print('There is no image to process')
        return False

    # lets suppose that for this moment we could have pdf files with only one page
    image = image_reader[0]

    # Find all doors from image
    door_scanner = DoorScanner()
    if not door_scanner.scan(image):
        print('Cannot find any door into given image')
        return False

    door_detection_image = image.copy()
    for (ex, ey, ew, eh) in door_scanner:
        print('Door -> ', ex, ey, ew, eh)
        cv2.rectangle(door_detection_image, (ex, ey), (ex + ew, ey + eh), (0, 0, 255), 2)

    cv2.imwrite(
        ProjectConfigurator.get_storage_path() + '/temp/' + out_path + '_door_results.jpg', door_detection_image
    )

    # Find all beton wall from image
    wall_scanner = WallScanner()

    if not wall_scanner.scan(image):
        print('Cannot find any door in given image')
        return False

    wall_scanner_image = image.copy()
    for wall in wall_scanner:
        paint_color = (randint(0, 255), randint(0, 255), randint(0, 255))
        cv2.drawContours(wall_scanner_image, [wall], -1, paint_color, 3)

    cv2.imwrite(ProjectConfigurator.get_storage_path() + '/temp/' + out_path + '_wall_results.jpg', wall_scanner_image)

    return True


def main():
    logging.basicConfig(level=logging.WARNING)
    # nas2 = ExternalStorage('nas2')

    # Download storage content from nas2
    # if not nas2.download_storage_content():
    #     print('Cannot download storage content from remote server')
    #     return

    # Call main function
    process()

    # Remove build_classifier from remote
    # nas2.remove_from_remote('build_classifier')

    # Upload storage content to nas2
    # if not nas2.upload_storage_content():
    #     print('Cannot upload storage content to remote server')
    #     return


if __name__ == '__main__':
    main()
