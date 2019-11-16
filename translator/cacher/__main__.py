import os
import requests
from os import path
from urllib.parse import urljoin

from . import settings
from . import emojis

KEY = settings.value("azure", "face", "key")
ENDPOINT = settings.value("azure", "face", "endpoint")


def main():
    for emoji in emojis.parse():
        print(emoji)


def api_call(picture):
    url = urljoin(
        ENDPOINT, "/face/v1.0/detect?returnFaceId=false&returnFaceAttributes=emotion"
    )
    data = {"url": picture}
    headers = {"Ocp-Apim-Subscription-Key": KEY}

    response = requests.post(url, headers=headers, json=data)

    return response.json()


if __name__ == "__main__":
    main()
