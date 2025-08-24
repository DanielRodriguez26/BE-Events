from datetime import datetime, timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.db.models import Event, Role
from app.db.models import Session as SessionModel
from app.db.models import Speaker, User


@pytest.fixture
def sample_event(test_db: Session) -> Event:
    """Create a sample event for testing."""
    event = Event(
        title="Test Conference 2024",
        description="A test conference for session testing",
        location="Test Venue",
        start_date=datetime.now() + timedelta(days=30),  # Evento en el futuro
        end_date=datetime.now() + timedelta(days=31),
        capacity=100,
        is_active=True,
    )
    test_db.add(event)
    test_db.commit()
    test_db.refresh(event)
    return event


@pytest.fixture
def sample_speaker(test_db: Session) -> Speaker:
    """Create a sample speaker for testing."""
    speaker = Speaker(
        name="John Doe",
        bio="Experienced speaker in technology",
        email="john.doe@example.com",
        phone="+34 600 000 001",
        company="Tech Corp",
        is_active=True,
    )
    test_db.add(speaker)
    test_db.commit()
    test_db.refresh(speaker)
    return speaker


@pytest.fixture
def sample_session(
    test_db: Session, sample_event: Event, sample_speaker: Speaker
) -> SessionModel:
    """Create a sample session for testing."""
    session = SessionModel(
        title="Introduction to Python",
        description="Learn the basics of Python programming",
        start_time=sample_event.start_date + timedelta(hours=1),
        end_time=sample_event.start_date + timedelta(hours=2),
        capacity=50,
        event_id=sample_event.id,
        speaker_id=sample_speaker.id,
        is_active=True,
    )
    test_db.add(session)
    test_db.commit()
    test_db.refresh(session)
    return session


class TestSessionReadOperations:
    """Test session read operations."""

    def test_get_all_sessions_empty(self, client: TestClient):
        """Test getting all sessions when database is empty."""
        response = client.get("/api/v1/sessions/")
        assert response.status_code == 200
        data = response.json()
        assert data["items"] == []
        assert data["total_items"] == 0
        assert data["page"] == 1

    def test_get_all_sessions_with_data(
        self, client: TestClient, sample_session: SessionModel
    ):
        """Test getting all sessions with data in database."""
        response = client.get("/api/v1/sessions/")
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 1
        assert data["total_items"] == 1
        assert data["items"][0]["title"] == "Introduction to Python"

    def test_get_session_by_id_found(
        self, client: TestClient, sample_session: SessionModel
    ):
        """Test getting a session by ID when it exists."""
        response = client.get(f"/api/v1/sessions/{sample_session.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Introduction to Python"
        assert data["id"] == sample_session.id

    def test_get_session_by_id_not_found(self, client: TestClient):
        """Test getting a session by ID when it doesn't exist."""
        response = client.get("/api/v1/sessions/999")
        assert response.status_code == 404

    def test_get_sessions_by_event(
        self, client: TestClient, sample_session: SessionModel, sample_event: Event
    ):
        """Test getting sessions for a specific event."""
        response = client.get(f"/api/v1/sessions/event/{sample_event.id}")
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["event_id"] == sample_event.id

    def test_get_sessions_by_event_empty(self, client: TestClient, sample_event: Event):
        """Test getting sessions for an event with no sessions."""
        response = client.get(f"/api/v1/sessions/event/{sample_event.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["items"] == []
        assert data["total_items"] == 0


class TestSessionCreateOperations:
    """Test session creation operations."""

    def test_create_session_success(
        self, client: TestClient, sample_event: Event, sample_speaker: Speaker
    ):
        """Test creating a session successfully."""
        # Asegurar que las horas estén en intervalos de 30 minutos y en el futuro
        future_time = datetime.now() + timedelta(days=1)
        start_time = future_time.replace(minute=0, second=0, microsecond=0)
        end_time = start_time + timedelta(hours=1)

        session_data = {
            "title": "Advanced Python",
            "description": "Advanced Python programming concepts",
            "event_id": sample_event.id,
            "speaker_id": sample_speaker.id,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "capacity": 30,
        }

        response = client.post("/api/v1/sessions/", json=session_data)
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.json()}")
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Advanced Python"
        assert data["event_id"] == sample_event.id
        assert data["speaker_id"] == sample_speaker.id
        assert data["capacity"] == 30

    def test_create_session_without_speaker(
        self, client: TestClient, sample_event: Event
    ):
        """Test creating a session without assigning a speaker."""
        # Asegurar que las horas estén en intervalos de 30 minutos y en el futuro
        future_time = datetime.now() + timedelta(days=1)
        start_time = future_time.replace(minute=30, second=0, microsecond=0)
        end_time = start_time + timedelta(hours=1)

        session_data = {
            "title": "Open Discussion",
            "description": "Open discussion session",
            "event_id": sample_event.id,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "capacity": 100,
        }

        response = client.post("/api/v1/sessions/", json=session_data)
        assert response.status_code == 200
        data = response.json()
        assert data["speaker_id"] is None

    def test_create_session_invalid_event(
        self, client: TestClient, sample_speaker: Speaker
    ):
        """Test creating a session with non-existent event."""
        # Asegurar que las horas estén en intervalos de 30 minutos y en el futuro
        future_time = datetime.now() + timedelta(days=1)
        start_time = future_time.replace(minute=0, second=0, microsecond=0)
        end_time = start_time + timedelta(hours=1)

        session_data = {
            "title": "Test Session",
            "description": "Test description",
            "event_id": 999,  # Non-existent event
            "speaker_id": sample_speaker.id,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "capacity": 50,
        }

        response = client.post("/api/v1/sessions/", json=session_data)
        assert response.status_code == 400
        assert "Event with id 999 does not exist" in response.json()["detail"]

    def test_create_session_invalid_speaker(
        self, client: TestClient, sample_event: Event
    ):
        """Test creating a session with non-existent speaker."""
        # Asegurar que las horas estén en intervalos de 30 minutos y en el futuro
        future_time = datetime.now() + timedelta(days=1)
        start_time = future_time.replace(minute=0, second=0, microsecond=0)
        end_time = start_time + timedelta(hours=1)

        session_data = {
            "title": "Test Session",
            "description": "Test description",
            "event_id": sample_event.id,
            "speaker_id": 999,  # Non-existent speaker
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "capacity": 50,
        }

        response = client.post("/api/v1/sessions/", json=session_data)
        assert response.status_code == 400
        assert "Speaker with id 999 does not exist" in response.json()["detail"]

    def test_create_session_outside_event_dates(
        self, client: TestClient, sample_event: Event, sample_speaker: Speaker
    ):
        """Test creating a session outside the event date range."""
        # Asegurar que las horas estén en intervalos de 30 minutos
        outside_time = sample_event.end_date + timedelta(days=1)
        start_time = outside_time.replace(minute=0, second=0, microsecond=0)
        end_time = start_time + timedelta(hours=1)

        session_data = {
            "title": "Test Session",
            "description": "Test description",
            "event_id": sample_event.id,
            "speaker_id": sample_speaker.id,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "capacity": 50,
        }

        response = client.post("/api/v1/sessions/", json=session_data)
        assert response.status_code == 400
        assert (
            "Session schedule must be within the event's date range"
            in response.json()["detail"]
        )

    def test_create_session_schedule_conflict(
        self,
        client: TestClient,
        sample_session: SessionModel,
        sample_event: Event,
        sample_speaker: Speaker,
    ):
        """Test creating a session with schedule conflict."""
        # Try to create a session that overlaps with the existing one
        # Asegurar que las horas estén en intervalos de 30 minutos
        start_time = sample_session.start_time + timedelta(minutes=30)
        start_time = start_time.replace(minute=0, second=0, microsecond=0)
        end_time = start_time + timedelta(hours=1)

        session_data = {
            "title": "Conflicting Session",
            "description": "This should conflict",
            "event_id": sample_event.id,
            "speaker_id": sample_speaker.id,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "capacity": 50,
        }

        response = client.post("/api/v1/sessions/", json=session_data)
        assert response.status_code == 400
        assert "Schedule conflict with existing sessions" in response.json()["detail"]

    def test_create_session_invalid_times(
        self, client: TestClient, sample_event: Event, sample_speaker: Speaker
    ):
        """Test creating a session with invalid time range."""
        # Asegurar que las horas estén en intervalos de 30 minutos
        future_time = datetime.now() + timedelta(days=1)
        start_time = future_time.replace(minute=0, second=0, microsecond=0)
        end_time = start_time - timedelta(hours=1)  # End before start

        session_data = {
            "title": "Invalid Time Session",
            "description": "End time before start time",
            "event_id": sample_event.id,
            "speaker_id": sample_speaker.id,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),  # End before start
            "capacity": 50,
        }

        response = client.post("/api/v1/sessions/", json=session_data)
        assert response.status_code == 422  # Validation error

    def test_create_session_negative_capacity(
        self, client: TestClient, sample_event: Event, sample_speaker: Speaker
    ):
        """Test creating a session with negative capacity."""
        # Asegurar que las horas estén en intervalos de 30 minutos y en el futuro
        future_time = datetime.now() + timedelta(days=1)
        start_time = future_time.replace(minute=0, second=0, microsecond=0)
        end_time = start_time + timedelta(hours=1)

        session_data = {
            "title": "Negative Capacity Session",
            "description": "Test negative capacity",
            "event_id": sample_event.id,
            "speaker_id": sample_speaker.id,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "capacity": -10,
        }

        response = client.post("/api/v1/sessions/", json=session_data)
        assert response.status_code == 422  # Validation error


class TestSessionUpdateOperations:
    """Test session update operations."""

    def test_update_session_success(
        self, client: TestClient, sample_session: SessionModel
    ):
        """Test updating a session successfully."""
        update_data = {
            "title": "Updated Python Session",
            "description": "Updated description",
            "capacity": 75,
        }

        response = client.put(f"/api/v1/sessions/{sample_session.id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Python Session"
        assert data["description"] == "Updated description"
        assert data["capacity"] == 75

    def test_update_session_not_found(self, client: TestClient):
        """Test updating a session that doesn't exist."""
        update_data = {"title": "Updated Title"}

        response = client.put("/api/v1/sessions/999", json=update_data)
        assert response.status_code == 404

    def test_update_session_schedule_conflict(
        self,
        client: TestClient,
        sample_session: SessionModel,
        sample_event: Event,
        sample_speaker: Speaker,
    ):
        """Test updating a session to create a schedule conflict."""
        # Create another session first
        other_session = SessionModel(
            title="Other Session",
            description="Another session",
            start_time=sample_event.start_date + timedelta(hours=3),
            end_time=sample_event.start_date + timedelta(hours=4),
            capacity=50,
            event_id=sample_event.id,
            speaker_id=sample_speaker.id,
            is_active=True,
        )
        from sqlalchemy.orm import object_session

        db = object_session(sample_session)
        db.add(other_session)
        db.commit()

        # Try to update the first session to conflict with the second
        # Asegurar que las horas estén en intervalos de 30 minutos
        start_time = other_session.start_time + timedelta(minutes=30)
        start_time = start_time.replace(minute=0, second=0, microsecond=0)
        end_time = start_time + timedelta(hours=1)

        update_data = {
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
        }

        response = client.put(f"/api/v1/sessions/{sample_session.id}", json=update_data)
        assert response.status_code == 400
        assert "Schedule conflict with existing sessions" in response.json()["detail"]


class TestSessionDeleteOperations:
    """Test session delete operations."""

    def test_delete_session_success(
        self, client: TestClient, sample_session: SessionModel
    ):
        """Test deleting a session successfully."""
        response = client.delete(f"/api/v1/sessions/{sample_session.id}")
        assert response.status_code == 200
        assert response.json()["message"] == "Session deleted successfully"

    def test_delete_session_not_found(self, client: TestClient):
        """Test deleting a session that doesn't exist."""
        response = client.delete("/api/v1/sessions/999")
        assert response.status_code == 404


class TestEventSessionEndpoints:
    """Test session endpoints within events context."""

    def test_get_event_sessions(
        self, client: TestClient, sample_session: SessionModel, sample_event: Event
    ):
        """Test getting sessions for a specific event via event endpoint."""
        response = client.get(f"/api/v1/events/{sample_event.id}/sessions")
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["event_id"] == sample_event.id

    def test_create_event_session(
        self,
        client: TestClient,
        sample_event: Event,
        sample_speaker: Speaker,
        organizer_headers: dict,
    ):
        """Test creating a session for a specific event."""
        # Asegurar que las horas estén en intervalos de 30 minutos y en el futuro
        future_time = datetime.now() + timedelta(days=1)
        start_time = future_time.replace(minute=0, second=0, microsecond=0)
        end_time = start_time + timedelta(hours=1)

        session_data = {
            "title": "Event Session",
            "description": "Session created via event endpoint",
            "speaker_id": sample_speaker.id,
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "capacity": 40,
        }

        response = client.post(
            f"/api/v1/events/{sample_event.id}/sessions",
            json=session_data,
            headers=organizer_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Event Session"
        assert data["event_id"] == sample_event.id
