import json
from math import sqrt

from PIL import Image, ImageOps

from . import emojis
from .utils import cache
from .api import find_emotions, search_images


def get_rectangle(rect, scale):
    left = rect.left
    top = rect.top
    right = left + rect.height
    bottom = top + rect.width

    # expand margins
    ox = left + 0.5 * rect.height
    oy = top + 0.5 * rect.width
    expleft = ox - (rect.height / 2) * scale
    exptop = oy - (rect.width / 2) * scale
    expright = ox + (rect.height / 2) * scale
    expbottom = oy + (rect.width / 2) * scale

    return (expleft, exptop, expright, expbottom)


class Face:
    def __init__(self, filename):
        self.filename = filename

        img = Image.open(self.filename)
        self.filename = self.filename[:(len(self.filename) - 4)] + ".jpg"
        img = self.rotate_if_exif_specifies(img)
        width, height = img.size
        img = img.resize((width,height), Image.NEAREST)
        img = img.resize((width, height), Image.NEAREST)
        img.save(self.filename, "JPEG", compress_level=9)

        self.emotions, box = find_emotions(self.filename, file=True)

        img = Image.open(self.filename)
        rect_coords = get_rectangle(box, 1.5)
        self.cropped = img.crop(rect_coords)
        self.cropped = ImageOps.fit(self.cropped, (128, 128), method=Image.ANTIALIAS)

    def rotate_if_exif_specifies(self, image):
        try:
            exif_tags = image._getexif()
            if exif_tags is None:
                # No EXIF tags, so we don't need to rotate
                print('No EXIF data, so not transforming')
                return image

            value = exif_tags[274]
        except KeyError:
            # No rotation tag present, so we don't need to rotate
            print('EXIF data present but no rotation tag, so not transforming')
            return image

        value_to_transform = {
            1: (0, False),
            2: (0, True),
            3: (180, False),
            4: (180, True),
            5: (-90, True),
            6: (-90, False),
            7: (90, True),
            8: (90, False)
        }

        try:
            angle, flip = value_to_transform[value]
        except KeyError:
            print(f'EXIF rotation \'{value}\' unknown, not transforming')
            return image

        print(f'EXIF rotation \'{value}\' detected, rotating {angle} degrees, flip: {flip}')
        if angle != 0:
            image = image.rotate(angle)

        if flip:
            image = image.tranpose(Image.FLIP_LEFT_RIGHT)

        return image

class EmojiModel:
    def __init__(self, faces):
        self.emojis = None
        with cache("model.json") as f:
            if not f.writable():
                self.emojis = json.load(f)
            else:
                self.emojis = self.load_emojis()
                json.dump(self.emojis, f, indent=4)

        self.faces = faces

    def emoji_to_face(self, emoji):
        if emoji.name not in self.emojis:
            return None
        center = self.emojis[emoji.name]

        best = None
        best_dist = None
        for face in self.faces:
            dist = emotion_dist(center, face.emotions)
            if best is None or dist < best_dist:
                best = face
                best_dist = dist

        return best

    def load_emojis(self):
        centers = {}
        for emoji in emojis.parse():
            if emoji.group != "Smileys & Emotion" or "face" not in emoji.name:
                continue

            sums = {}
            total = 0
            for image in search_images(emoji.clean_name + " human person", 5):
                emotions, _ = find_emotions(image)
                if not emotions:
                    continue

                total += 1
                for key, value in emotions.items():
                    if key not in sums:
                        sums[key] = value
                    else:
                        sums[key] += value

            for key in sums:
                sums[key] /= total

            if sums:
                centers[emoji.name] = sums

        return centers


def emotion_dist(first, second):
    total = 0
    for emotion in first:
        total += (first[emotion] - second[emotion]) ** 2
    return sqrt(total)
