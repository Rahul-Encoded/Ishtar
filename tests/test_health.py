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