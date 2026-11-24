from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_list_machines():
    response = client.get("/machines")

    assert response.status_code == 200
    assert len(response.json()) == 3

def test_get_machine():
    response = client.get("/machines/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_machine_not_found():
    response = client.get("/machines/999")

    assert response.status_code == 404

def test_invalid_machine_id():
    response = client.get("/machines/abc")

    assert response.status_code == 422

def test_alarms_found():
    response = client.get("/machines/1/alarms")

    assert response.status_code == 200
    
    alarms = response.json()

    assert len(alarms) > 0
    assert alarms[0]["machine_id"] == 1
    