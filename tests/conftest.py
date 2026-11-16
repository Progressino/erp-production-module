"""Shared fixtures for the standalone Production Module test suite."""
from __future__ import annotations

import pytest
from starlette.testclient import TestClient


@pytest.fixture
def client(isolated_module_dbs):
    """FastAPI TestClient wired to the standalone production main.py."""
    from backend.main import app
    with TestClient(app, raise_server_exceptions=True) as c:
        yield c
