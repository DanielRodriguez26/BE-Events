"""
User registration tests.

This module contains tests for user registration functionality.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.db.models import Role, User


class TestUserRegistration:
    """Test user registration functionality."""

    def test_register_user_success(self, client, test_db, sample_role):
        """Test successful user registration."""
        # Test data
        user_data = {
            "username": "newuser_test",
            "email": "newuser@test.com",
            "password": "securepass123",
            "first_name": "New",
            "last_name": "User",
            "phone": "+34 600 000 999",
            "is_active": True,
            "role_id": sample_role.id,
        }

        # Test registration
        response = client.post("/api/v1/auth/register", json=user_data)

        assert response.status_code == 200
        data = response.json()

        # Check response structure
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["username"] == "newuser_test"
        assert data["email"] == "newuser@test.com"
        assert data["role"] == "user"
        assert "user_id" in data
        assert "expires_in" in data

        # Verify user was created in database
        user = test_db.query(User).filter(User.username == "newuser_test").first()
        assert user is not None
        assert user.email == "newuser@test.com"
        assert user.first_name == "New"
        assert user.last_name == "User"
        assert user.phone == "+34 600 000 999"
        assert user.is_active is True
        assert user.role_id == sample_role.id

    def test_register_user_duplicate_username(self, client, test_db, sample_role):
        """Test registration with duplicate username."""
        # Create existing user
        existing_user = User(
            username="existinguser",
            email="existing@test.com",
            password=get_password_hash("testpass123"),
            first_name="Existing",
            last_name="User",
            phone="+34 600 000 888",
            role_id=sample_role.id,
            is_active=True,
        )
        test_db.add(existing_user)
        test_db.commit()

        # Try to register with same username
        user_data = {
            "username": "existinguser",  # Duplicate username
            "email": "different@test.com",
            "password": "securepass123",
            "first_name": "Different",
            "last_name": "User",
            "phone": "+34 600 000 777",
            "is_active": True,
            "role_id": sample_role.id,
        }

        response = client.post("/api/v1/auth/register", json=user_data)

        assert response.status_code == 400
        assert "Username already exists" in response.json()["detail"]

    def test_register_user_duplicate_email(self, client, test_db, sample_role):
        """Test registration with duplicate email."""
        # Create existing user
        existing_user = User(
            username="existinguser2",
            email="existing2@test.com",
            password=get_password_hash("testpass123"),
            first_name="Existing",
            last_name="User",
            phone="+34 600 000 888",
            role_id=sample_role.id,
            is_active=True,
        )
        test_db.add(existing_user)
        test_db.commit()

        # Try to register with same email
        user_data = {
            "username": "differentuser",  # Different username
            "email": "existing2@test.com",  # Duplicate email
            "password": "securepass123",
            "first_name": "Different",
            "last_name": "User",
            "phone": "+34 600 000 777",
            "is_active": True,
            "role_id": sample_role.id,
        }

        response = client.post("/api/v1/auth/register", json=user_data)

        assert response.status_code == 400
        assert "Email already exists" in response.json()["detail"]

    def test_register_user_missing_required_fields(self, client, test_db, sample_role):
        """Test registration with missing required fields."""
        # Test missing username
        user_data_missing_username = {
            "email": "test@test.com",
            "password": "securepass123",
            "first_name": "Test",
            "last_name": "User",
            "phone": "+34 600 000 777",
            "is_active": True,
            "role_id": sample_role.id,
        }

        response = client.post("/api/v1/auth/register", json=user_data_missing_username)
        assert response.status_code == 422  # Validation error

        # Test missing email
        user_data_missing_email = {
            "username": "testuser",
            "password": "securepass123",
            "first_name": "Test",
            "last_name": "User",
            "phone": "+34 600 000 777",
            "is_active": True,
            "role_id": sample_role.id,
        }

        response = client.post("/api/v1/auth/register", json=user_data_missing_email)
        assert response.status_code == 422  # Validation error

        # Test missing password
        user_data_missing_password = {
            "username": "testuser",
            "email": "test@test.com",
            "first_name": "Test",
            "last_name": "User",
            "phone": "+34 600 000 777",
            "is_active": True,
            "role_id": sample_role.id,
        }

        response = client.post("/api/v1/auth/register", json=user_data_missing_password)
        assert response.status_code == 422  # Validation error

    def test_register_user_invalid_email_format(self, client, test_db, sample_role):
        """Test registration with invalid email format."""
        user_data = {
            "username": "testuser",
            "email": "invalid-email",  # Invalid email format
            "password": "securepass123",
            "first_name": "Test",
            "last_name": "User",
            "phone": "+34 600 000 777",
            "is_active": True,
            "role_id": sample_role.id,
        }

        response = client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 422  # Validation error

    def test_register_user_with_admin_role(self, client, test_db, sample_admin_role):
        """Test registration with admin role."""
        user_data = {
            "username": "adminuser_test",
            "email": "admin@test.com",
            "password": "securepass123",
            "first_name": "Admin",
            "last_name": "User",
            "phone": "+34 600 000 666",
            "is_active": True,
            "role_id": sample_admin_role.id,
        }

        response = client.post("/api/v1/auth/register", json=user_data)

        assert response.status_code == 200
        data = response.json()
        assert data["role"] == "admin"
        assert data["username"] == "adminuser_test"

    def test_register_user_inactive_by_default(self, client, test_db, sample_role):
        """Test registration with inactive user."""
        user_data = {
            "username": "inactiveuser_test",
            "email": "inactive@test.com",
            "password": "securepass123",
            "first_name": "Inactive",
            "last_name": "User",
            "phone": "+34 600 000 555",
            "is_active": False,  # Inactive user
            "role_id": sample_role.id,
        }

        response = client.post("/api/v1/auth/register", json=user_data)

        # Should still register successfully but return error on login attempt
        assert response.status_code == 200

        # Verify user was created as inactive
        user = test_db.query(User).filter(User.username == "inactiveuser_test").first()
        assert user is not None
        assert user.is_active is False

    def test_register_user_password_hashing(self, client, test_db, sample_role):
        """Test that password is properly hashed during registration."""
        user_data = {
            "username": "passwordtest_user",
            "email": "passwordtest@test.com",
            "password": "plaintextpassword",
            "first_name": "Password",
            "last_name": "Test",
            "phone": "+34 600 000 444",
            "is_active": True,
            "role_id": sample_role.id,
        }

        response = client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 200

        # Verify password was hashed
        user = test_db.query(User).filter(User.username == "passwordtest_user").first()
        assert user is not None
        assert user.password != "plaintextpassword"  # Should be hashed
        assert len(user.password) > 20  # Hashed passwords are longer

    def test_register_user_with_special_characters(self, client, test_db, sample_role):
        """Test registration with special characters in names."""
        user_data = {
            "username": "special_user",
            "email": "special@test.com",
            "password": "securepass123",
            "first_name": "José María",
            "last_name": "García-López",
            "phone": "+34 600 000 333",
            "is_active": True,
            "role_id": sample_role.id,
        }

        response = client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 200

        # Verify special characters were preserved
        user = test_db.query(User).filter(User.username == "special_user").first()
        assert user is not None
        assert user.first_name == "José María"
        assert user.last_name == "García-López"
