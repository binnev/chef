from collections import namedtuple

import pytest
from typer.testing import CliRunner

from src.cli import app

DEFAULT = """
config: 
    merge_ingredients: True
""".lstrip()

UPDATED = """
config: 
    merge_ingredients: False
""".lstrip()


@pytest.mark.better_parametrize(
    testcase := namedtuple("_", "cmd, expected, id"),
    [
        testcase(
            id="list",
            cmd="config",
            expected=DEFAULT,
        ),
        testcase(
            id="update with same value",
            cmd="config --merge-ingredients=True",
            expected=DEFAULT,
        ),
        testcase(
            id="update with same value (case insensitive)",
            cmd="config --merge-ingredients=true",
            expected=DEFAULT,
        ),
        testcase(
            id="update with different value",
            cmd="config --merge-ingredients=False",
            expected=UPDATED,
        ),
        testcase(
            id="update with different value (case insensitive)",
            cmd="config --merge-ingredients=false",
            expected=UPDATED,
        ),
    ],
)
def test_config__list(
    cmd: str,
    expected: str,
    mock_settings_save,
    recipe_library_initialised,
):
    runner = CliRunner()
    result = runner.invoke(app, cmd.split())
    assert result.exit_code == 0
    assert result.output == expected
    mock_settings_save.assert_called()
