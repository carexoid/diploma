from dotenv import load_dotenv
from google.cloud import vision

# export env variable with google auth key
load_dotenv()

client = vision.ImageAnnotatorClient()


def get_info(photo):
    image = vision.Image(content=photo)

    # TODO: apply geo params to raise accuracy of detection
    # web_detection_params = vision.WebDetectionParams(
    #     include_geo_results=True)
    # image_context = vision.ImageContext(
    #     web_detection_params=web_detection_params)

    response = client.web_detection(image=image)
    return response.web_detection.web_entities
