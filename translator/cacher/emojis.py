import re
import requests
import os
from os import path

from .utils import cache


EMOJI = "https://www.unicode.org/Public/emoji/12.0/emoji-test.txt"


EMOJI_REGEX = re.compile("^(\S+(?:\s\S+)*) *; *(\S*) *# *(\S+) (.*)")

GROUP_REGEX = re.compile("^# (sub)?group: (.*)")


def parse():
    with cache("emoji.txt") as f:
        if f.writable():
            content = requests.get(EMOJI).text
            f.write(content)
            lines = content.split("\n")
        else:
            lines = f

        group = None
        subgroup = None
        for line in lines:
            line = line.strip()

            # update group
            match = GROUP_REGEX.match(line)
            if match:
                if match.group(1) == "sub":
                    subgroup = match.group(2)
                else:
                    group = match.group(2)
                continue

            # ignore empty or commented lines
            if not line or line.startswith("#"):
                continue

            match = EMOJI_REGEX.match(line)
            parts = {
                "content": match.group(3),
                "codepoint": match.group(1),
                "status": match.group(2),
                "name": match.group(4),
                "group": group,
                "subgroup": subgroup,
            }

            emoji = Emoji(**parts)
            yield emoji


def _download():
    filename = "emoji.txt"
    with cache(filename) as f:
        if not f:
            return

    return filename


class Emoji:
    def __init__(self, content, codepoint, status, name, group=None, subgroup=None):
        self.content = content
        self.codepoint = codepoint
        self.status = status
        self.name = name

        self.group = group
        self.subgroup = subgroup

    @property
    def clean_name(self):
        parts = self.name.split()
        removal = ["face", "with", "eyes"]
        for target in removal:
            try:
                parts.remove(target)
            except ValueError:
                pass
        return " ".join(parts)

    def __str__(self):
        return f"<Emoji {self.content}>"
