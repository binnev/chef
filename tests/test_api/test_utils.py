from pathlib import Path

from api.utils import clean_filename


import pytest


@pytest.mark.parametrize(
    "filename, expected",
    [
        ("", ""),
        ("file.txt", "file.txt"),
        ("this-is-ok.bin", "this-is-ok.bin"),
        ("replace_underscores.txt", "replace-underscores.txt"),
        ("robin's recipe.md", "robins-recipe.md"),
        ("robin's recipe v2.md", "robins-recipe-v2.md"),
    ],
)
def test_clean_filename(filename: str, expected: str):
    assert clean_filename(Path(filename)) == Path(expected)
