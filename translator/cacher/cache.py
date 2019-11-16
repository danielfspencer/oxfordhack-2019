import os
from os import path


def cache(filename, *args, force=False):
    os.makedirs(".cache", exist_ok=True)
    location = path.join(".cache", filename)

    if not path.exists(location) or force:
        return open(location, *args)
    else:
        return Dummy()


class Dummy:
    def __bool__(self):
        return False

    def __enter__(self):
        pass

    def __exit__(self, *args):
        pass
