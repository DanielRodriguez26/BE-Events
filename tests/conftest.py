"""
Pytest configuration and fixtures.

This module contains common fixtures and configuration for all tests.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.security import get_password_hash
from app.db.base import Base, get_db
from app.db.models import Role, User
from app.main import app

# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def db_engine():
    """Create database engine for testing."""
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session(db_engine):
    """Create database session for testing."""
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(db_session):
    """Create test client with database session."""

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def test_db(db_session):
    """Test database session fixture."""
    return db_session


@pytest.fixture
def sample_role(db_session):
    """Create a sample role for testing."""
    role = Role(name="assistant")
    db_session.add(role)
    db_session.commit()
    db_session.refresh(role)
    return role


@pytest.fixture
def sample_admin_role(db_session):
    """Create a sample admin role for testing."""
    role = Role(name="admin")
    db_session.add(role)
    db_session.commit()
    db_session.refresh(role)
    return role


@pytest.fixture
def sample_organizer_role(db_session):
    """Create a sample organizer role for testing."""
    role = Role(name="organizer")
    db_session.add(role)
    db_session.commit()
    db_session.refresh(role)
    return role


@pytest.fixture
def sample_user(db_session, sample_role):
    """Create a sample user for testing."""
    user = User(
        username="testuser",
        email="test@example.com",
        password=get_password_hash("testpass123"),
        first_name="Test",
        last_name="User",
        phone="+34 600 000 000",
        role_id=sample_role.id,
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def sample_admin_user(db_session, sample_admin_role):
    """Create a sample admin user for testing."""
    user = User(
        username="adminuser",
        email="admin@example.com",
        password=get_password_hash("adminpass123"),
        first_name="Admin",
        last_name="User",
        phone="+34 600 000 001",
        role_id=sample_admin_role.id,
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def sample_organizer_user(db_session, sample_organizer_role):
    """Create a sample organizer user for testing."""
    user = User(
        username="organizeruser",
        email="organizer@example.com",
        password=get_password_hash("organizerpass123"),
        first_name="Organizer",
        last_name="User",
        phone="+34 600 000 002",
        role_id=sample_organizer_role.id,
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def valid_user_data(sample_role):
    """Valid user data for registration tests."""
    return {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "securepass123",
        "first_name": "New",
        "last_name": "User",
        "phone": "+34 600 000 999",
        "is_active": True,
        "role_id": sample_role.id,
    }


@pytest.fixture
def auth_headers(sample_user, client):
    """Get authentication headers for a test user."""
    # Login to get token
    response = client.post(
        "/api/v1/auth/login",
        json={"username": sample_user.username, "password": "testpass123"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def admin_headers(sample_admin_user, client):
    """Get authentication headers for an admin user."""
    # Login to get token
    response = client.post(
        "/api/v1/auth/login",
        json={"username": sample_admin_user.username, "password": "adminpass123"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def organizer_headers(sample_organizer_user, client):
    """Get authentication headers for an organizer user."""
    # Login to get token
    response = client.post(
        "/api/v1/auth/login",
        json={
            "username": sample_organizer_user.username,
            "password": "organizerpass123",
        },
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
