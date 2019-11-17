import os
import requests
import json
from pprint import pprint

KEY = os.environ['COGNITIVE_SERVICE_KEY']
ENDPOINT = os.environ['FACE_ENDPOINT']
face_api_url = '{}face/v1.0/detect'.format(ENDPOINT)

image_url = ''

headers = {'Ocp-Apim-Subscription-Key': KEY}

params = {
    'returnFaceId': 'false',
    'returnFaceLandmarks': 'true',
    'returnFaceAttributes': '',
}

response = requests.post(face_api_url, params=params,
                         headers=headers, json={"url": image_url})

data = response.json()[0]['faceLandmarks']
pprint(data)
