from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_get_sprints():
    response = client.get("/test-platform/")
    assert response.status_code == 200
    print(response.json())

test_get_sprints()
