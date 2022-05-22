import numpy as np
import cv2


def filter_noise(image):
    nparr = np.fromstring(image, np.uint8)
    image_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    filtered = cv2.medianBlur(image_np, 5)
    return cv2.imencode('.jpg', filtered)[1].tobytes()
