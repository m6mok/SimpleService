from unittest.mock import MagicMock

import pytest
from flask import Flask


@pytest.fixture
def mock_app():
    app = MagicMock(spec=Flask)
    app.logger = MagicMock()
    return app


@pytest.fixture
def mock_gunicorn(monkeypatch):
    mock = MagicMock()
    monkeypatch.setattr("simpleservice.main.BaseApplication", mock)
    return mock
