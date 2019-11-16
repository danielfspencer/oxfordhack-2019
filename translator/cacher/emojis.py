import re
import requests
import os
from os import path

EMOJI = "https://www.unicode.org/Public/emoji/12.0/emoji-test.txt"


EMOJI_REGEX = re.compile("^(\S+(?:\s\S+)*) *; *(\S*) *# *(\S+) (.*)")


def parse():
    _ensure_cached()
    with open(".cache/emoji.txt") as f:
        for line in f:
            line = line.strip()

            # ignore empty or commented lines
            if not line or line.startswith("#"):
                continue

            # print(line)

            match = EMOJI_REGEX.match(line)
            parts = {
                "content": match.group(3),
                "codepoint": match.group(1),
                "status": match.group(2),
                "name": match.group(4),
            }

            emoji = Emoji(**parts)
            yield emoji


def _ensure_cached():
    os.makedirs(".cache", exist_ok=True)

    if not path.exists(".cache/emoji.txt"):
        with open(".cache/emoji.txt", "w") as f:
            resp = requests.get(EMOJI)
            f.write(resp.text)


class Emoji:
    def __init__(self, content, codepoint, status, name):
        self.content = content
        self.codepoint = codepoint
        self.status = status
        self.name = name

    def __str__(self):
        return f"<Emoji {self.content}>"
