#!/usr/bin/env python3
"""
Script para probar la inserción de datos en la base de datos
"""

from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.db.base import SessionLocal
from app.db.models import Event


def test_database_insert():
    """Probar la inserción de un evento en la base de datos"""

    print("=== PRUEBA DE INSERCIÓN EN BASE DE DATOS ===")

    # Crear una sesión de base de datos
    db = SessionLocal()

    try:
        # Crear datos de evento de prueba
        test_event_data = {
            "title": "Evento de Prueba",
            "description": "Este es un evento de prueba para verificar la conexión a la base de datos",
            "location": "Sala de Pruebas",
            "start_date": datetime.now() + timedelta(days=1),
            "end_date": datetime.now() + timedelta(days=1, hours=2),
            "capacity": 50,
            "is_active": True,
        }

        print(f"1. Creando evento con datos: {test_event_data['title']}")

        # Crear el evento
        event = Event(**test_event_data)
        db.add(event)
        db.commit()
        db.refresh(event)

        print(f"   ✅ Evento creado exitosamente con ID: {event.id}")

        # Verificar que el evento se guardó correctamente
        print("\n2. Verificando que el evento se guardó...")
        saved_event = db.query(Event).filter(Event.id == event.id).first()

        if saved_event:
            print(f"   ✅ Evento encontrado en la base de datos:")
            print(f"      - ID: {saved_event.id}")
            print(f"      - Título: {saved_event.title}")
            print(f"      - Descripción: {saved_event.description}")
            print(f"      - Ubicación: {saved_event.location}")
            print(f"      - Capacidad: {saved_event.capacity}")
            print(f"      - Activo: {saved_event.is_active}")
        else:
            print("   ❌ Error: El evento no se encontró en la base de datos")

        # Contar todos los eventos
        print("\n3. Contando eventos en la base de datos...")
        total_events = db.query(Event).count()
        print(f"   Total de eventos en la base de datos: {total_events}")

        # Limpiar el evento de prueba
        print("\n4. Limpiando evento de prueba...")
        db.delete(event)
        db.commit()
        print("   ✅ Evento de prueba eliminado")

    except Exception as e:
        print(f"   ❌ Error durante la prueba: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    test_database_insert()
