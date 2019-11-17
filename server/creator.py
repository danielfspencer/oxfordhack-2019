import os

from translator import translator
from translator import emojis
from translator.translator import Face
from translator.api import find_emotions

from font import compose


def create(image_directory):
    faces = []
    for image in os.listdir(image_directory)[:10]:
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

    with open("master_emoji_list", "r") as f:
        for emoji in emojis.parse_lines(f):
            result = model.emoji_to_face(emoji)
            if not result:
                continue

            results.append((emoji.codepoint.lower(), result.data))

    compose.build_font(results, os.path.join(image_directory, "font.ttf"))
