from pathlib import Path
from unittest.mock import patch, MagicMock

from src.api import init_library
from src.api.constants import __app_name__


@patch("src.api.initialise.open")
@patch("src.api.initialise.Path.mkdir")
@patch("src.api.initialise.Path.exists", return_value=False)
def test_init_library__new(
    mock_exists: MagicMock,
    mock_mkdir: MagicMock,
    mock_open: MagicMock,
):
    path = Path("foo/bar")
    init_library(path)
    assert mock_mkdir.call_count == 4
    assert [call.args[0] for call in mock_mkdir.call_args_list] == [
        path,
        path / "yaml",
        path / "md",
        path / f".{__app_name__}",
    ]
    mock_open.assert_called_with(path / ".yes-chef/settings.json", "w")
    mock_exists.assert_called()


@patch("src.api.initialise.open")
@patch("src.api.initialise.Path.mkdir")
@patch("src.api.initialise.Path.exists", return_value=True)
def test_init_library__existing(
    mock_exists: MagicMock,
    mock_mkdir: MagicMock,
    mock_open: MagicMock,
):
    path = Path("foo/bar")
    init_library(path)
    assert mock_mkdir.call_count == 4
    mock_open.assert_not_called()
    mock_exists.assert_called()
