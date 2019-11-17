import json
from math import sqrt


from . import emojis
from .utils import cache
from .api import find_emotions, search_images


class Face:
    def __init__(self, emotions, data):
        self.emotions = emotions
        self.data = data


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
