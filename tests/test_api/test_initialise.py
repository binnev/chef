from pathlib import Path
from unittest.mock import patch, MagicMock

from src.api import init_library
from src.api.constants import __app_name__


@patch("src.api.initialise.open")
@patch("src.api.initialise.Path.exists", return_value=False)
def test_init_library__new(
    mock_exists: MagicMock,
    mock_open: MagicMock,
    mock_path_mkdir: MagicMock,
):
    path = Path("foo/bar")
    init_library(path)
    assert mock_path_mkdir.call_count == 4
    assert [call.args[0] for call in mock_path_mkdir.call_args_list] == [
        path,
        path / "yaml",
        path / "md",
        path / f".{__app_name__}",
    ]
    mock_open.assert_called_with(path / ".yes-chef/settings.json", "w")
    mock_exists.assert_called()


def test_init_library__updates_settings(mock_settings_load: MagicMock):
    mock_settings = MagicMock()
    mock_settings_load.return_value = mock_settings

    path = Path("foo/bar")
    init_library(path)

    assert mock_settings.system.recipe_library == path


@patch("src.api.initialise.open")
@patch("src.api.initialise.Path.exists", return_value=True)
def test_init_library__existing(
    mock_exists: MagicMock,
    mock_open: MagicMock,
    mock_path_mkdir: MagicMock,
):
    path = Path("foo/bar")
    init_library(path)
    assert mock_path_mkdir.call_count == 4
    mock_open.assert_not_called()
    mock_exists.assert_called()
