from unittest.mock import MagicMock

import pytest

from api.settings import Settings


@pytest.fixture(autouse=True)
def mock_settings_save(request, monkeypatch):
    """
    Make sure we don't create real settings files when running tests 
    """
    
    if "allow_settings_save" in request.keywords: 
        return 
    
    monkeypatch.setattr(Settings, "save", MagicMock())
