from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from api.settings import Settings, GLOBAL_SETTINGS_FILE, BASE

pytestmark = pytest.mark.allow_settings_save


@patch("api.settings.utils.touch")
@patch("api.settings.open")
def test_save(mock_open, mock_touch):
    mock_file = MagicMock()

    class MockOpenFileContext:
        def __enter__(self):
            return mock_file

        def __exit__(self, *args, **kwargs):
            pass

    mock_open.return_value = MockOpenFileContext()

    settings = Settings()
    settings.save()

    mock_touch.assert_called_with(GLOBAL_SETTINGS_FILE)
    mock_open.assert_called_with(GLOBAL_SETTINGS_FILE, "w")
    mock_file.write.assert_called_once()
    assert mock_file.write.call_args.args[0].startswith('{"recipe_library')


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
@patch("api.settings.open")
def test_from_file(
        mock_open,
        json_string: str,
        expected_library_path: Path,
):
    mock_file = MagicMock()
    mock_file.read.return_value = json_string

    class MockOpenFileContext:
        def __enter__(self):
            return mock_file

        def __exit__(self, *args, **kwargs):
            pass

    mock_open.return_value = MockOpenFileContext()

    settings = Settings.from_file()
    assert settings.recipe_library == expected_library_path

    mock_open.assert_called_with(GLOBAL_SETTINGS_FILE)
    mock_file.read.assert_called_once_with()
