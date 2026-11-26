import pytest
from fastapi.testclient import TestClient

from app import store
from app.main import app


@pytest.fixture(autouse=True)
def reset_items_store():
    """Reset the in-memory store before each test."""
    store.reset_store()
    yield
    store.reset_store()


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client
