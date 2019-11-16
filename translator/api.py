import requests
import os
from urllib.parse import urljoin

from .utils import settings

from . import face_client
from . import bing_client


def find_emotions(picture):
    try:
        faces = face_client.face.detect_with_url(
            url=picture, return_face_attributes=["emotion"]
        )
    except:
        return None

    if not faces:
        return None

    emotions = faces[0].face_attributes.emotion.as_dict()
    return emotions


def search_images(term, count=None):
    images = bing_client.images.search(query=term + " human person", count=count)
    return [image.content_url for image in images.value]
