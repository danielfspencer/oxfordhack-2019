import sys
import os
from os import path


def cache(filename, force=False):
    os.makedirs(".cache", exist_ok=True)
    location = path.join(".cache", filename)

    if not path.exists(location) or force:
        return open(location, "w")
    else:
        return open(location, "r")


def settings(*parts: str) -> str:
    key = "_".join(parts).upper()

    if key in os.environ:
        return os.environ[key]
    else:
        print(f"Set the {key} environment variable", file=sys.stderr)
        sys.exit(-1)
