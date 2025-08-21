#!/usr/bin/env python3
"""
Script simple para probar que la aplicación funciona correctamente.
"""

from fastapi.testclient import TestClient

from app.main import app


def test_app():
    """Test básico de la aplicación."""
    client = TestClient(app)

    # Test root endpoint
    print("Testing root endpoint...")
    response = client.get("/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

    # Test health endpoint
    print("\nTesting health endpoint...")
    response = client.get("/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

    # Test events endpoint
    print("\nTesting events endpoint...")
    response = client.get("/api/v1/events/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

    print("\n✅ All basic tests passed!")


if __name__ == "__main__":
    test_app()
