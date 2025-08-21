from datetime import datetime, timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base, get_db
from app.db.models import Event
from app.main import app

# Create test database
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1234@localhost:5432/myevents"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create test tables
Base.metadata.create_all(bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture
def test_db():
    """Create test database and clean up after tests."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def sample_event_data():
    """Sample event data for testing."""
    return {
        "title": "Test Event",
        "description": "This is a test event",
        "location": "Test Location",
        "start_date": datetime.now() + timedelta(days=1),
        "end_date": datetime.now() + timedelta(days=1, hours=2),
        "capacity": 100,
        "is_active": True,
    }


def test_get_all_events_empty(test_db):
    """Test getting all events when database is empty."""
    response = client.get("/api/v1/events/")
    assert response.status_code == 200
    assert response.json() == []


def test_get_all_events_with_data(test_db, sample_event_data):
    """Test getting all events with data in database."""
    # Create a test event directly in database
    db = TestingSessionLocal()
    event = Event(**sample_event_data)
    db.add(event)
    db.commit()
    db.close()

    response = client.get("/api/v1/events/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == sample_event_data["title"]


def test_get_event_by_id_not_found(test_db):
    """Test getting event by ID when it doesn't exist."""
    response = client.get("/api/v1/events/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Event not found"


def test_get_event_by_id_found(test_db, sample_event_data):
    """Test getting event by ID when it exists."""
    # Create a test event directly in database
    db = TestingSessionLocal()
    event = Event(**sample_event_data)
    db.add(event)
    db.commit()
    event_id = event.id
    db.close()

    response = client.get(f"/api/v1/events/{event_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == sample_event_data["title"]
    assert data["id"] == event_id


def test_root_endpoint():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Welcome to Events API"


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
