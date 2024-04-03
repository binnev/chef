from pathlib import Path
from unittest.mock import MagicMock

import pytest

from src.api.settings import Settings


@pytest.fixture(autouse=True)
def mock_settings_save(request, monkeypatch):
    """
    Make sure we don't create real settings files when running tests
    """

    if "allow_settings_save" in request.keywords:
        return

    mock = MagicMock()
    monkeypatch.setattr(Settings, "save", mock)
    return mock


@pytest.fixture(autouse=True)
def mock_settings_load(request, monkeypatch):
    """
    Make sure we don't create real settings files when running tests
    """

    if "allow_settings_load" in request.keywords:
        return

    mock = MagicMock()
    mock.return_value = Settings()
    monkeypatch.setattr(Settings, "load", mock)
    return mock


@pytest.fixture(autouse=True)
def mock_path_mkdir(request, monkeypatch):
    """
    Don't allow creating dirs with `Path.mkdir()` in tests
    """
    if "allow_path_mkdir" in request.keywords:
        return

    mock = MagicMock()
    monkeypatch.setattr(Path, "mkdir", mock)
    return mock


@pytest.fixture(autouse=True)
def mock_path_touch(request, monkeypatch):
    """
    Don't allow creating files with `Path.touch()` in tests
    """
    if "allow_path_touch" in request.keywords:
        return

    mock = MagicMock()
    monkeypatch.setattr(Path, "touch", mock)
    return mock


@pytest.fixture(autouse=True)
def mock_path_glob(request, monkeypatch):
    """
    Don't allow tests to change behaviour based on the results of `Path.glob()`
    """
    if "allow_path_glob" in request.keywords:
        return

    mock = MagicMock()
    mock.return_value = (_ for _ in [])  # Path.glob returns a generator
    monkeypatch.setattr(Path, "glob", mock)
    return mock


@pytest.fixture
def mock_open_file_ctx():
    class MockOpenFileContext:
        mock_file: MagicMock

        def __init__(self):
            super().__init__()
            self.mock_file = MagicMock()

        def __enter__(self):
            return self.mock_file

        def __exit__(self, *args, **kwargs):
            pass

    mock_ctx = MockOpenFileContext()

    yield mock_ctx
