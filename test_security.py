#!/usr/bin/env python3
"""
Script de prueba para el sistema de seguridad de la API de Eventos.

Este script demuestra cómo usar la autenticación y autorización
con diferentes roles de usuario.
"""

import json
from typing import Any, Dict

import requests

# Configuración
BASE_URL = "http://localhost:8000/api/v1"
HEADERS = {"Content-Type": "application/json"}


def print_response(response: requests.Response, title: str = ""):
    """Imprime la respuesta de manera formateada."""
    print(f"\n{'='*50}")
    if title:
        print(f"📋 {title}")
    print(f"{'='*50}")
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except:
        print(f"Response: {response.text}")
    print(f"{'='*50}")


def test_public_endpoints():
    """Prueba endpoints públicos (sin autenticación)."""
    print("\n🔓 PROBANDO ENDPOINTS PÚBLICOS")

    # GET /events/ (público)
    response = requests.get(f"{BASE_URL}/events/")
    print_response(response, "GET /events/ (Público)")

    # GET /events/search (público)
    response = requests.get(f"{BASE_URL}/events/search")
    print_response(response, "GET /events/search (Público)")


def test_protected_endpoints_without_auth():
    """Prueba endpoints protegidos sin autenticación."""
    print("\n🚫 PROBANDO ENDPOINTS PROTEGIDOS SIN AUTENTICACIÓN")

    # POST /events/ sin token
    event_data = {
        "title": "Evento de Prueba",
        "description": "Este evento no debería crearse",
        "location": "Ciudad de Prueba",
        "date": "2024-12-25T10:00:00",
        "is_active": True,
    }

    response = requests.post(f"{BASE_URL}/events/", json=event_data, headers=HEADERS)
    print_response(response, "POST /events/ sin token (debe fallar)")

    # DELETE /events/1 sin token
    response = requests.delete(f"{BASE_URL}/events/1", headers=HEADERS)
    print_response(response, "DELETE /events/1 sin token (debe fallar)")


def get_token(username: str, password: str) -> str:
    """Obtiene un token de autenticación."""
    login_data = {"username": username, "password": password}

    response = requests.post(f"{BASE_URL}/auth/login", json=login_data, headers=HEADERS)

    if response.status_code == 200:
        token_data = response.json()
        print(f"✅ Login exitoso para {username}")
        print(f"   Role: {token_data.get('role', 'N/A')}")
        return token_data["access_token"]
    else:
        print(f"❌ Login fallido para {username}")
        print_response(response, f"Login {username}")
        return None


def test_organizer_permissions():
    """Prueba permisos de organizador."""
    print("\n👤 PROBANDO PERMISOS DE ORGANIZADOR")

    # Obtener token de organizador
    token = get_token("organizer@ejemplo.com", "password123")
    if not token:
        print("❌ No se pudo obtener token de organizador")
        return

    headers = {**HEADERS, "Authorization": f"Bearer {token}"}

    # POST /events/ (debe funcionar)
    event_data = {
        "title": "Evento del Organizador",
        "description": "Evento creado por un organizador",
        "location": "Centro de Eventos",
        "date": "2024-12-30T15:00:00",
        "is_active": True,
    }

    response = requests.post(f"{BASE_URL}/events/", json=event_data, headers=headers)
    print_response(response, "POST /events/ como Organizador (debe funcionar)")

    # PUT /events/1 (debe funcionar)
    update_data = {
        "title": "Evento Actualizado por Organizador",
        "description": "Descripción actualizada",
    }

    response = requests.put(f"{BASE_URL}/events/1", json=update_data, headers=headers)
    print_response(response, "PUT /events/1 como Organizador (debe funcionar)")

    # DELETE /events/1 (debe fallar - solo admin)
    response = requests.delete(f"{BASE_URL}/events/1", headers=headers)
    print_response(response, "DELETE /events/1 como Organizador (debe fallar)")


def test_admin_permissions():
    """Prueba permisos de administrador."""
    print("\n👑 PROBANDO PERMISOS DE ADMINISTRADOR")

    # Obtener token de admin
    token = get_token("admin@ejemplo.com", "admin123")
    if not token:
        print("❌ No se pudo obtener token de administrador")
        return

    headers = {**HEADERS, "Authorization": f"Bearer {token}"}

    # GET /users/ (solo admin)
    response = requests.get(f"{BASE_URL}/users/", headers=headers)
    print_response(response, "GET /users/ como Admin (debe funcionar)")

    # DELETE /events/1 (solo admin)
    response = requests.delete(f"{BASE_URL}/events/1", headers=headers)
    print_response(response, "DELETE /events/1 como Admin (debe funcionar)")


def test_user_permissions():
    """Prueba permisos de usuario básico."""
    print("\n👤 PROBANDO PERMISOS DE USUARIO BÁSICO")

    # Obtener token de usuario
    token = get_token("user@ejemplo.com", "password123")
    if not token:
        print("❌ No se pudo obtener token de usuario")
        return

    headers = {**HEADERS, "Authorization": f"Bearer {token}"}

    # POST /events/ (debe fallar)
    event_data = {
        "title": "Evento del Usuario",
        "description": "Este evento no debería crearse",
        "location": "Ciudad",
        "date": "2024-12-25T10:00:00",
        "is_active": True,
    }

    response = requests.post(f"{BASE_URL}/events/", json=event_data, headers=headers)
    print_response(response, "POST /events/ como Usuario (debe fallar)")

    # GET /users/ (debe fallar)
    response = requests.get(f"{BASE_URL}/users/", headers=headers)
    print_response(response, "GET /users/ como Usuario (debe fallar)")


def test_invalid_token():
    """Prueba con token inválido."""
    print("\n🚫 PROBANDO CON TOKEN INVÁLIDO")

    headers = {**HEADERS, "Authorization": "Bearer token_invalido_123"}

    response = requests.post(f"{BASE_URL}/events/", json={}, headers=headers)
    print_response(response, "POST /events/ con token inválido (debe fallar)")


def main():
    """Función principal que ejecuta todas las pruebas."""
    print("🔐 SISTEMA DE PRUEBAS DE SEGURIDAD - API DE EVENTOS")
    print("=" * 60)

    try:
        # Probar endpoints públicos
        test_public_endpoints()

        # Probar endpoints protegidos sin autenticación
        test_protected_endpoints_without_auth()

        # Probar con token inválido
        test_invalid_token()

        # Probar permisos de diferentes roles
        test_user_permissions()
        test_organizer_permissions()
        test_admin_permissions()

        print("\n✅ Todas las pruebas completadas!")
        print("\n📝 RESUMEN:")
        print("- Los endpoints públicos funcionan sin autenticación")
        print("- Los endpoints protegidos requieren autenticación válida")
        print("- Los roles tienen permisos específicos:")
        print("  • user: solo puede ver eventos")
        print("  • organizer: puede crear y actualizar eventos")
        print("  • admin: puede hacer todo, incluyendo eliminar eventos")

    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al servidor.")
        print("   Asegúrate de que el servidor esté corriendo en http://localhost:8000")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")


if __name__ == "__main__":
    main()
