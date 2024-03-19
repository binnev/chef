import json
from collections import namedtuple
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from src.api.settings import (
    Settings,
    GLOBAL_SETTINGS_FILE,
    get_or_create_json,
    DEFAULT_RECIPE_LIBRARY,
)

DEFAULTS = Settings().model_dump()


@pytest.mark.allow_settings_save
@patch("src.api.settings.utils.touch")
@patch("src.api.settings.open")
def test_save(mock_open, mock_touch, mock_open_file_ctx):
    mock_open.return_value = mock_open_file_ctx

    settings = Settings()
    settings.save()

    mock_touch.assert_called_with(GLOBAL_SETTINGS_FILE)
    mock_open.assert_called_with(GLOBAL_SETTINGS_FILE, "w")
    mock_open_file_ctx.mock_file.write.assert_called_once()
    assert mock_open_file_ctx.mock_file.write.call_args.args[0].startswith(
        '{"recipe_library'
    )


@pytest.mark.allow_settings_load
@pytest.mark.better_parametrize(
    testcase := namedtuple(
        "_",
        "global_settings, user_settings, expected_settings, id",
    ),
    [
        testcase(
            id="all empty",
            global_settings={},
            user_settings={},
            expected_settings=DEFAULTS,
        ),
        testcase(
            id="only global settings",
            global_settings={"recipe_library": "some/path"},
            user_settings={},
            expected_settings=DEFAULTS | {"recipe_library": Path("some/path")},
        ),
        testcase(
            id="only user settings",
            global_settings={},
            user_settings={"recipe_library": "some/path"},
            expected_settings=DEFAULTS | {"recipe_library": Path("some/path")},
        ),
        testcase(
            id="user settings override globals",
            global_settings={"recipe_library": "old/path"},
            user_settings={"recipe_library": "some/path"},
            expected_settings=DEFAULTS | {"recipe_library": Path("some/path")},
        ),
        testcase(
            id="bogus user settings should be ignored",
            global_settings={},
            user_settings={"foo": "bar"},
            expected_settings=DEFAULTS,
        ),
    ],
)
@patch("src.api.settings.get_or_create_json")
def test_load(
    mock_json,
    global_settings: dict,
    user_settings: dict,
    expected_settings: dict,
):
    mock_json.side_effect = [
        global_settings,
        user_settings,
    ]
    settings = Settings.from_file()
    assert settings.model_dump() == expected_settings

    assert mock_json.call_args_list[0].args[0] == GLOBAL_SETTINGS_FILE
    assert (
        mock_json.call_args_list[1].args[0]
        == DEFAULT_RECIPE_LIBRARY / ".yes-chef/settings.json"
    )


@pytest.mark.better_parametrize(
    testcase := namedtuple("_", "json_string, side_effect, expected, id"),
    [
        testcase(
            id="File exists but is empty",
            json_string="",
            side_effect=None,
            expected=json.JSONDecodeError("", "", 0),
        ),
        testcase(
            id="Outer object is array",
            json_string='[{"foo": "bar"}]',
            side_effect=None,
            expected=ValueError(
                """JSON shouldn't be an array: [{"foo": "bar"}]"""
            ),
        ),
        testcase(
            id="File not found",
            json_string="",
            side_effect=[
                FileNotFoundError,  # first open attempt (read mode)
                MagicMock(),  # second open attempt (write mode)
            ],
            expected={},
        ),
        testcase(
            id="Success: empty dictionary",
            json_string="{}",
            side_effect=None,
            expected={},
        ),
        testcase(
            id="Success: non-empty dictionary",
            json_string='{"foo": "bar"}',
            side_effect=None,
            expected={"foo": "bar"},
        ),
    ],
)
@patch("src.api.settings.open")
def test_get_or_create_json(
    mock_open,
    json_string: str,
    side_effect: Exception | None,
    expected: type[Exception] | None,
    mock_open_file_ctx,
):
    mock_open_file_ctx.mock_file.read.return_value = json_string
    mock_open.return_value = mock_open_file_ctx
    mock_open.side_effect = side_effect
    path = Path("foo/bar.json")

    if isinstance(expected, Exception):
        with pytest.raises(expected.__class__):
            get_or_create_json(path)
    else:
        assert get_or_create_json(path) == expected
