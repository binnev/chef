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


@pytest.fixture
def mock_open_file():
    mock_file = MagicMock()

    class MockOpenFileContext:
        def __enter__(self):
            return mock_file

        def __exit__(self, *args, **kwargs):
            pass

    mock_ctx = MockOpenFileContext()

    yield mock_file, mock_ctx
