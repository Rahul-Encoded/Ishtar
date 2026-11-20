from fastapi.testclient import TestClient
from jarvis.main import app

test_client = TestClient(app)

def test_health() -> None:
    response = test_client.get("/health")
    assert response.status_code == 200
    print(f"DATA: {response.json()}")
    data = response.json()
    print(f"DATA2: {data}")
    assert data["status"] == "ok"
    assert data["version"] == "1.0.0"
    assert "timestamp" in data

def test_chat_valid_message() -> None:
    response = test_client.post("/chat", json={"message": "Hello, Ishtar!"})
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Ishtar recieved your message: Hello, Ishtar!"
    assert "timestamp" in data

def test_chat_empty_message() -> None:
    response = test_client.post("/chat", json={"message": ""})
    assert response.status_code == 422
    data = response.json()
    assert data["detail"][0]["msg"] == "String should have at least 1 character"
    assert data["detail"][0]["type"] == "string_too_short"
    assert "timestamp" not in data