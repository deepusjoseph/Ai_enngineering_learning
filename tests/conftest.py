import pytest
from fastapi.testclient import TestClient

from phase_0_baseline.main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)
