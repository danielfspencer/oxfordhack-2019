import itertools
import json
from math import sqrt

from . import emojis
from .cache import cache
from .api import search_images, find_emotions

IMAGE = ""


def main():
    m = model()

    will = find_emotions(IMAGE)
    print(will)

    best = None
    best_dist = None
    for emoji_name, position in m.items():
        dist = 0
        for emotion in position:
            dist += (position[emotion] - will[emotion]) ** 2
        dist = sqrt(dist)

        if best is None or dist < best_dist:
            best = emoji_name
            best_dist = dist

    print(best)
    print(best_dist)


def model():
    with cache("model.json") as f:
        if not f.writable():
            return json.load(f)

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

        json.dump(centers, f, indent=4)
        return centers


if __name__ == "__main__":
    main()
