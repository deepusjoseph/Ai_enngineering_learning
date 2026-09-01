from fastapi.testclient import TestClient

from phase_0_baseline.main import app

client = TestClient(app)


def test_root() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Phase 0 Baseline API is running",
    }


def test_echo() -> None:
    response = client.post(
        "/echo",
        json={
            "message": "Hello AI",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello AI",
        "length": 8,
    }


def test_echo_requires_message() -> None:
    response = client.post("/echo", json={})

    assert response.status_code == 422


def test_stream() -> None:
    response = client.get("/stream")

    assert response.status_code == 200
    assert response.text == "Hello from streaming!"