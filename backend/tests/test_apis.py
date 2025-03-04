

from fastapi.testclient import TestClient
from backend.app.main import app
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from typing import List

client = TestClient(app)

def test_get_sprints():
    response = client.get("/test-platform/")
    assert response.status_code == 200
    print(response.json())


def test_generate_rn():
    # Correct data format, sending the sprints as a part of the JSON payload
    data = {"sprints": ['Sprint 28', 'Sprint 29']}
    response = client.post(url='/generate/', json=data)  # Use `json=data` instead of `data=[...]`

    # Validate response status code
    # assert response.status_code == 200

    # Optionally, print the response or assert on other properties of the response
    print(response.json())


test_generate_rn()
