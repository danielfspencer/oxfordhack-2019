import requests
import os
from urllib.parse import urljoin

from .utils import settings

from . import face_client
from . import bing_client


def find_emotions(picture, file=False):
    if file:
        with open(picture, "r+b") as f:
            faces = face_client.face.detect_with_stream(
                f, return_face_attributes=["emotion"]
            )
    else:
        faces = face_client.face.detect_with_url(
            url=picture, return_face_attributes=["emotion"]
        )

    if not faces:
        return None, None

    emotions = faces[0].face_attributes.emotion.as_dict()
    box = faces[0].face_rectangle
    return emotions, box


def find_bounding_boxes(picture, file=False):
    if file:
        with open(picture, "r+b") as f:
            faces = face_client.face.detect_with_stream(f)
    else:
        faces = face_client.face.detect_with_url(url=picture)

    return [face.face_rectangle for face in faces]


def search_images(term, count=None):
    images = bing_client.images.search(query=term + " human person", count=count)
    return [image.content_url for image in images.value]
