import os
from os import path


def cache(filename, force=False):
    os.makedirs(".cache", exist_ok=True)
    location = path.join(".cache", filename)

    if not path.exists(location) or force:
        return open(location, "w")
    else:
        return open(location, "r")
