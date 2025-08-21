#!/usr/bin/env python3
"""
Script para probar los endpoints y verificar la conexión a la base de datos
"""

import json
from datetime import datetime, timedelta

import requests

# URL base de la API
BASE_URL = "http://localhost:8000"


def test_endpoints():
    """Probar los endpoints principales"""

    print("=== PRUEBA DE ENDPOINTS ===")

    # 1. Probar endpoint raíz
    print("\n1. Probando endpoint raíz...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")

    # 2. Probar health check
    print("\n2. Probando health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")

    # 3. Probar obtener todos los eventos
    print("\n3. Probando obtener todos los eventos...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/events/")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")

    # 4. Probar obtener evento por ID (debería fallar con 404)
    print("\n4. Probando obtener evento por ID inexistente...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/events/999")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")


if __name__ == "__main__":
    test_endpoints()
