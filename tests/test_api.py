#!/usr/bin/env python3
from datetime import datetime, timezone
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_get_events_starts_empty():
    response = client.get("/events/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_and_get_event():
    payload = {
        "title": "Evento de Prueba",
        "description": "Este es un evento de prueba",
        "date": datetime.now(timezone.utc).isoformat(),
        "location": "Madrid",
        "is_active": True,
    }
    created = client.post("/events/", json=payload)
    assert created.status_code == 201
    data = created.json()
    assert data["title"] == payload["title"]
    event_id = data["id"]

    fetched = client.get(f"/events/{event_id}")
    assert fetched.status_code == 200
    assert fetched.json()["id"] == event_id

    updated = client.put(f"/events/{event_id}", json={"title": "Actualizado"})
    assert updated.status_code == 200
    assert updated.json()["title"] == "Actualizado"

    deleted = client.delete(f"/events/{event_id}")
    assert deleted.status_code == 204
