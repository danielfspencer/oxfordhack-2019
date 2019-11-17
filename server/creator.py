import os

import shutil
from translator import translator
from translator import emojis
from translator.translator import Face

from font import compose
from separator import separator

def create(image_directory):
    separator.init()

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

    used_faces = []
    with open("master_emoji_list", "r") as f:
        for emoji in emojis.parse_lines(f):
            result = model.emoji_to_face(emoji)
            if result and not result in used_faces:
                result.cropped.save(result.filename)
                bg_removed = result.filename + ".bg_rem.png"
                cropped = result.filename + ".crop.png"

                separator.seperate(result.filename, bg_removed)

                img = Image.open(bg_removed)
                cropped_img = ImageOps.fit(img, (128, 128), method=Image.ANTIALIAS)
                cropped_img.save(cropped)

                result.filename = cropped

                used_faces.append(result)


    with open("master_emoji_list", "r") as f:
        for emoji in emojis.parse_lines(f):
            result = model.emoji_to_face(emoji)
            if not result:
                continue

            results.append((emoji.codepoint.lower(), result.filename))

    serve_dir = os.path.join(image_directory, "serve")
    shutil.copytree("font/tester/", serve_dir)
    compose.build_font(results, os.path.join(serve_dir, "test.ttf"))
