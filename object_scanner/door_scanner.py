import cv2
from rubik.project_configurator import ProjectConfigurator


class DoorScanner:
    """
        This object is used in order to find doors into a given image
    """
    def __init__(self):
        """
            Initialize DoorScanner object
        """
        self.__classifier_path = ProjectConfigurator.get_path_from_storage('classifiers/door_classifier.xml')

        # create cascade object from xml file
        self.__classifier_object = cv2.CascadeClassifier(self.__classifier_path)

        # initialize resulting boxes
        self.__objects = []

    def scan(self, image):
        """
            Scan a image in order to find door locations

            @param image:   Image as numpy array (opencv style)
            @return:        True if image was successfully scanned or false otherwise
        """
        # reinitialize list of objects
        self.__objects = []

        # convert image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # convert gray image to binary
        binary_img = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)[1]

        detection_res = self.__classifier_object.detectMultiScale(binary_img,
                                                                  scaleFactor=1.3,
                                                                  minNeighbors=35,
                                                                  minSize=(100, 100),
                                                                  maxSize=(200, 200))
        for (ex, ey, ew, eh) in detection_res:
            self.__objects.append((ex, ey, ew, eh))

        return True

    def __len__(self):
        return len(self.__objects)

    def __getitem__(self, key):
        return self.__objects[key]


if __name__ == '__main__':
    ds = DoorScanner()
