from . import emojis
from . import translator
from .api import find_emotions

IMAGE = ""


def main():
    ems = list(emojis.parse())

    will = translator.Face(find_emotions(IMAGE), "will")

    m = translator.EmojiModel([will])
    res = m.emoji_to_face(ems[0])
    print(res.data)


if __name__ == "__main__":
    main()
