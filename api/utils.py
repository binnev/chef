from pathlib import Path


def touch(file: Path):
    file.parent.mkdir(exist_ok=True, parents=True)
    file.touch(exist_ok=True)
