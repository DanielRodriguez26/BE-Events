"""
Authentication tests.

This module contains tests for authentication and authorization functionality.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.security import create_access_token, get_password_hash
from app.db.models import Role, User
from app.main import app

client = TestClient(app)


class TestAuthentication:
    """Test authentication functionality."""

    def test_login_success(self, test_db: Session):
        """Test successful login."""
        # Get or create test role
        role = test_db.query(Role).filter(Role.name == "user").first()
        if not role:
            role = Role(name="user")
            test_db.add(role)
            test_db.commit()
            test_db.refresh(role)

        # Check if user already exists
        existing_user = (
            test_db.query(User).filter(User.username == "testuser_auth").first()
        )
        if not existing_user:
            # Create test user with unique email
            user = User(
                username="testuser_auth",
                email="test_auth@example.com",
                password=get_password_hash("testpass123"),
                first_name="Test",
                last_name="User",
                phone="+34 600 000 001",
                role_id=role.id,
                is_active=True,
            )
            test_db.add(user)
            test_db.commit()

        # Test login
        response = client.post(
            "/api/v1/auth/login",
            json={"username": "testuser_auth", "password": "testpass123"},
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["username"] == "testuser_auth"
        assert data["email"] == "test_auth@example.com"
        assert data["role"] == "user"

    def test_login_invalid_credentials(self, test_db: Session):
        """Test login with invalid credentials."""
        response = client.post(
            "/api/v1/auth/login",
            json={"username": "nonexistent", "password": "wrongpass"},
        )

        assert response.status_code == 401
        assert "Incorrect username or password" in response.json()["detail"]

    def test_login_inactive_user(self, test_db: Session):
        """Test login with inactive user."""
        # Get or create test role
        role = test_db.query(Role).filter(Role.name == "user").first()
        if not role:
            role = Role(name="user")
            test_db.add(role)
            test_db.commit()
            test_db.refresh(role)

        # Check if user already exists
        existing_user = (
            test_db.query(User).filter(User.username == "inactiveuser_auth").first()
        )
        if not existing_user:
            # Create test user with unique email
            user = User(
                username="inactiveuser_auth",
                email="inactive_auth@example.com",
                password=get_password_hash("testpass1234"),
                first_name="Inactive",
                last_name="User",
                phone="+34 600 000 002",
                role_id=role.id,
                is_active=False,
            )
            test_db.add(user)
            test_db.commit()

        # Test login
        response = client.post(
            "/api/v1/auth/login",
            json={"username": "inactiveuser_auth", "password": "testpass1234"},
        )

        assert response.status_code == 401
        assert "User account is deactivated" in response.json()["detail"]


@pytest.fixture
def test_db():
    """Test database fixture."""
    from app.db.base import SessionLocal

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
