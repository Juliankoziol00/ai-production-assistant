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

def test_get_stopped_machines():
    response = client.get("/machines/stopped")

    assert response.status_code == 200

    stopped_machines = response.json()

    assert type(stopped_machines) == list
    assert "CNC-02" in stopped_machines

def test_get_machine_summary():
    response = client.get("/machines/1/summary")

    assert response.status_code == 200

    summary = response.json()

    assert isinstance(summary, dict)
    assert summary["machine_id"] == 1
    assert "alarm_count" in summary

def test_get_non_existable_machine_summary():
    response = client.get("/machines/999/summary")

    assert response.status_code == 404

def test_get_machines_without_alarms():
    response = client.get("/machines/3/summary")

    assert response.status_code == 200
    
    summary = response.json()

    assert summary["alarm_count"] == 0