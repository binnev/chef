from pathlib import Path
from unittest.mock import patch

import pytest

from src.api.settings import Settings, GLOBAL_SETTINGS_FILE, BASE

pytestmark = pytest.mark.allow_settings_save


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


@pytest.mark.parametrize(
    "json_string, expected_library_path",
    [
        (
            '{"recipe_library":"some/path"}',
            Path("some/path"),
        ),
        (
            "",
            BASE.joinpath("recipes"),
        ),
    ],
)
@patch("src.api.settings.open")
def test_from_file(
    mock_open,
    json_string: str,
    expected_library_path: Path,
    mock_open_file_ctx,
):
    mock_open_file_ctx.mock_file.read.return_value = json_string
    mock_open.return_value = mock_open_file_ctx

    settings = Settings.from_file()
    assert settings.recipe_library == expected_library_path

    mock_open.assert_called_with(GLOBAL_SETTINGS_FILE)
    mock_open_file_ctx.mock_file.read.assert_called_once_with()
