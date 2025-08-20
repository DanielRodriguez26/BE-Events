#!/usr/bin/env python3
"""
Script de prueba para verificar que la API funciona correctamente.
"""
import requests
import json
from datetime import datetime, timezone

def test_health_endpoint():
    """Prueba el endpoint de health check."""
    try:
        response = requests.get("http://localhost:8000/health")
        print(f"✅ Health Check: {response.status_code}")
        print(f"   Response: {response.json()}")
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servidor. Asegúrate de que esté ejecutándose.")
        return False

def test_get_events():
    """Prueba el endpoint GET /events/."""
    try:
        response = requests.get("http://localhost:8000/events/")
        print(f"✅ GET /events/: {response.status_code}")
        print(f"   Response: {response.json()}")
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servidor.")
        return False

def test_create_event():
    """Prueba el endpoint POST /events/."""
    try:
        event_data = {
            "title": "Evento de Prueba",
            "description": "Este es un evento de prueba para verificar la API",
            "date": datetime.now(timezone.utc).isoformat(),
            "location": "Madrid, España",
            "is_active": True
        }
        
        response = requests.post(
            "http://localhost:8000/events/",
            json=event_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"✅ POST /events/: {response.status_code}")
        print(f"   Response: {response.json()}")
        return response.status_code == 201
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar al servidor.")
        return False

def main():
    """Ejecuta todas las pruebas."""
    print("🧪 Iniciando pruebas de la API...")
    print("=" * 50)
    
    # Verificar que el servidor esté ejecutándose
    if not test_health_endpoint():
        print("\n❌ El servidor no está ejecutándose.")
        print("   Ejecuta: python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
        return
    
    print("\n" + "=" * 50)
    
    # Probar endpoints
    test_get_events()
    test_create_event()
    
    print("\n" + "=" * 50)
    print("🎉 Pruebas completadas!")
    print("\n📋 Endpoints disponibles:")
    print("   - Health Check: http://localhost:8000/health")
    print("   - API Docs: http://localhost:8000/docs")
    print("   - Events: http://localhost:8000/events/")

if __name__ == "__main__":
    main()
