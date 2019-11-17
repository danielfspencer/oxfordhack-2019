import os

import shutil
from translator import translator
from translator import emojis
from translator.translator import Face

from font import compose


def create(image_directory):
    faces = []
    for image in os.listdir(image_directory)[:10]:
        if not (image.endswith(".png") or image.endswith(".jpg")):
            continue
        image = os.path.join(image_directory, image)

        print(image)

        face = Face(image)
        if face.cropped and face.emotions:
            faces.append(face)

    model = translator.EmojiModel(faces)

    results = []

    with open("master_emoji_list", "r") as f:
        for emoji in emojis.parse_lines(f):
            result = model.emoji_to_face(emoji)
            if not result:
                continue

            cropped_location = result.filename + ".smaller.png"
            result.cropped.save(cropped_location)
            results.append((emoji.codepoint.lower(), cropped_location))

    serve_dir = os.path.join(image_directory, "serve")
    shutil.copytree("font/tester/", serve_dir)
    compose.build_font(results, os.path.join(serve_dir, "test.ttf"))
