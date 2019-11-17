import json
from math import sqrt

from PIL import Image, ImageOps

from . import emojis
from .utils import cache
from .api import find_emotions, search_images, find_bounding_boxes


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

        self.emotions = find_emotions(filename, file=True)

        boxes = find_bounding_boxes(filename, file=True)
        if len(boxes) == 1:
            img = Image.open(filename)
            rect_coords = get_rectangle(boxes[0], 1.5)
            self.cropped = img.crop(rect_coords)
            self.cropped = ImageOps.fit(
                self.cropped, (128, 128), method=Image.ANTIALIAS
            )
        else:
            self.cropped = None


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
                emotions = find_emotions(image)
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
