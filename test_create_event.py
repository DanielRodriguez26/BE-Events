#!/usr/bin/env python3
"""
Script para probar la creación de eventos a través del endpoint POST
"""

import json
from datetime import datetime, timedelta


def test_create_event():
    """Probar la creación de un evento a través del endpoint POST"""

    print("=== PRUEBA DE CREACIÓN DE EVENTO ===")

    # Datos del evento a crear
    event_data = {
        "title": "Evento de Prueba API",
        "description": "Este es un evento creado a través de la API para probar la base de datos",
        "location": "Sala de Conferencias",
        "start_date": (datetime.now() + timedelta(days=1)).isoformat(),
        "end_date": (datetime.now() + timedelta(days=1, hours=2)).isoformat(),
        "capacity": 100,
        "is_active": True,
    }

    print(f"1. Datos del evento a crear:")
    print(f"   - Título: {event_data['title']}")
    print(f"   - Descripción: {event_data['description']}")
    print(f"   - Ubicación: {event_data['location']}")
    print(f"   - Capacidad: {event_data['capacity']}")

    # Convertir a JSON
    json_data = json.dumps(event_data)

    print(f"\n2. Enviando solicitud POST a /api/v1/events/")
    print(f"   JSON: {json_data}")

    # Usar PowerShell para hacer la solicitud POST
    powershell_command = f"""
    $headers = @{{"Content-Type"="application/json"}}
    $body = '{json_data}'
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/events/" -Method POST -Headers $headers -Body $body
    $response | ConvertTo-Json -Depth 10
    """

    print(f"\n3. Ejecutando comando PowerShell...")
    print(f"   Comando: {powershell_command.strip()}")

    # Ejecutar el comando PowerShell
    import subprocess

    try:
        result = subprocess.run(
            ["powershell", "-Command", powershell_command],
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode == 0:
            print(f"   ✅ Respuesta exitosa:")
            print(f"   {result.stdout}")
        else:
            print(f"   ❌ Error en la solicitud:")
            print(f"   {result.stderr}")

    except Exception as e:
        print(f"   ❌ Error ejecutando el comando: {e}")


if __name__ == "__main__":
    test_create_event()
