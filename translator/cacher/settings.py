import os
import sys


def value(*parts: str) -> str:
    key = "_".join(parts).upper()

    if key in os.environ:
        return os.environ[key]
    else:
        print(f"Set the {key} environment variable", file=sys.stderr)
        sys.exit(-1)
