import io
import os

from dotenv import load_dotenv
from google.cloud import vision

# export env variable with google auth key
load_dotenv()

client = vision.ImageAnnotatorClient()


def get_info(photo):
    image = vision.Image(content=photo)

    response = client.label_detection(image=image)
    return response.label_annotations


# if __name__ == '__main__':
#
#     client = vision.ImageAnnotatorClient()
#
#     file_name = os.path.abspath('../../../../Desktop/index.jpeg')
#
#     # Loads the image into memory
#     with io.open(file_name, 'rb') as image_file:
#         content = image_file.read()
#
#     image = vision.Image(content=content)
#
#     # Performs label detection on the image file
#     response = client.label_detection(image=image)
#     labels = response.label_annotations
#     print('Labels:')
#     for label in labels:
#         print(label.description)
