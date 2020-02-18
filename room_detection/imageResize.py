import cv2


def image_resize(image, size=800, inter=cv2.INTER_AREA):
    (h, w) = image.shape[:2]
    width, height = None, None
    if h > w:
        height = size
    else:
        width = size
    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))
    resized = cv2.resize(image, dim, interpolation=inter)
    return resized
