import os

from translator import translator
from translator import emojis
from translator.translator import Face
from translator.api import find_emotions


def create(image_directory):
    faces = []
    for image in os.listdir(image_directory)[:20]:
        if not (image.endswith(".png") or image.endswith(".jpg")):
            continue
        image = os.path.join(image_directory, image)

        print(image)

        emotes = find_emotions(image, file=True)
        if emotes:
            face = Face(emotes, image)
            faces.append(face)

    model = translator.EmojiModel(faces)

    results = []
    for emoji in emojis.parse():
        result = model.emoji_to_face(emoji)
        if not result:
            continue

        results.append(result)
        print(result)

