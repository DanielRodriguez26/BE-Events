"""
Event tests.

This module contains tests for event functionality.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.db.models import Event, Role, User


class TestEvents:
    """Test event functionality."""

    def test_get_events(self, client: TestClient, test_db: Session):
        """Test getting all events."""
        response = client.get("/api/v1/events")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "page" in data
        assert "total_items" in data

    def test_create_event_unauthorized(self, client: TestClient):
        """Test creating event without authentication."""
        response = client.post(
            "/api/v1/events",
            json={
                "title": "Test Event",
                "description": "Test Description",
                "date": "2024-06-15T09:00:00",
                "location": "Test Location",
                "capacity": 100,
                "is_active": True,
            },
        )
        assert response.status_code == 403

    def test_create_event_authorized(
        self, client: TestClient, organizer_headers: dict, test_db: Session
    ):
        """Test creating event with authentication."""
        response = client.post(
            "/api/v1/events",
            json={
                "title": "Test Event",
                "description": "Test Description",
                "start_date": "2024-06-15T09:00:00",
                "end_date": "2024-06-15T17:00:00",
                "location": "Test Location",
                "capacity": 100,
                "is_active": True,
            },
            headers=organizer_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test Event"
        assert data["description"] == "Test Description"
        assert data["capacity"] == 100

    def test_get_event_by_id(self, client: TestClient, test_db: Session):
        """Test getting event by ID."""
        # First create an event
        role = test_db.query(Role).filter(Role.name == "organizer").first()
        if not role:
            role = Role(name="organizer")
            test_db.add(role)
            test_db.commit()
            test_db.refresh(role)

        user = test_db.query(User).filter(User.email == "organizer@example.com").first()
        if not user:
            user = User(
                username="organizeruser",
                email="organizer@example.com",
                password="hashed_password",
                first_name="Organizer",
                last_name="User",
                phone="+34 600 000 002",
                role_id=role.id,
                is_active=True,
            )
            test_db.add(user)
            test_db.commit()
            test_db.refresh(user)

        from datetime import datetime

        event = Event(
            title="Test Event",
            description="Test Description",
            start_date=datetime.fromisoformat("2024-06-15T09:00:00"),
            end_date=datetime.fromisoformat("2024-06-15T17:00:00"),
            location="Test Location",
            capacity=100,
            is_active=True,
        )
        test_db.add(event)
        test_db.commit()
        test_db.refresh(event)

        # Test getting the event
        response = client.get(f"/api/v1/events/{event.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test Event"
        assert data["id"] == event.id

    def test_get_event_not_found(self, client: TestClient):
        """Test getting non-existent event."""
        response = client.get("/api/v1/events/99999")
        assert response.status_code == 404

    def test_search_events(self, client: TestClient):
        """Test searching events."""
        response = client.get("/api/v1/events/search?title=test")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_get_upcoming_events(self, client: TestClient):
        """Test getting upcoming events."""
        response = client.get("/api/v1/events/upcoming/with-capacity")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "page" in data
        assert "total_items" in data
