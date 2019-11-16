import json
import os
import requests
from urllib.parse import urljoin

from . import settings
from . import emojis
from .cache import cache

FACE_KEY = settings.value("azure", "face", "key")
FACE_ENDPOINT = settings.value("azure", "face", "endpoint")

BING_KEY = settings.value("azure", "bing", "key")
BING_ENDPOINT = settings.value("azure", "bing", "endpoint")


def main():
    content = {}

    targets = ["grinning person"]

    with cache("emotions.json", "w") as f:
        if not f:
            return

        for target in targets:
            results = {}
            for image in search_images(target, 5):
                emotions = find_emotions(image)
                results[image] = emotions
            content[target] = results

        json.dump(content, f, indent=4)


def find_emotions(picture):
    url = urljoin(FACE_ENDPOINT, "/face/v1.0/detect",)
    url += "?returnFaceId=false&returnFaceAttributes=emotion"
    data = {"url": picture}
    headers = {"Ocp-Apim-Subscription-Key": FACE_KEY}

    response = requests.post(url, headers=headers, json=data)
    faces = response.json()
    if faces:
        face = faces[0]
        return face["faceAttributes"]["emotion"]
    else:
        return None


def search_images(term, count=None):
    url = urljoin(BING_ENDPOINT, "/bing/v7.0/images/search")
    url += f"?q={term}"
    if count:
        url += f"&count={count}"
    headers = {"Ocp-Apim-Subscription-Key": BING_KEY}

    response = requests.get(url, headers=headers)
    return [image["contentUrl"] for image in response.json()["value"]]


if __name__ == "__main__":
    main()
