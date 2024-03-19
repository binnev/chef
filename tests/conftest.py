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

    monkeypatch.setattr(Settings, "save", MagicMock())


@pytest.fixture(autouse=True)
def mock_settings_load(request, monkeypatch):
    """
    Make sure we don't create real settings files when running tests
    """

    if "allow_settings_load" in request.keywords:
        return

    monkeypatch.setattr(Settings, "from_file", lambda: Settings())


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
