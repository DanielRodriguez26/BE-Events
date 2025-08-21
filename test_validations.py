#!/usr/bin/env python3
"""
Script para probar las validaciones del servicio de eventos sin depender de la base de datos.
"""

from datetime import datetime, timedelta
from unittest.mock import MagicMock, Mock

from sqlalchemy.orm import Session

from app.api.schemas.event_schemas import EventCreate
from app.services.event_service import EventService


def test_validations():
    """Test de las validaciones del servicio de eventos."""

    # Mock de la base de datos
    mock_db = Mock(spec=Session)
    mock_repository = Mock()

    # Configurar el mock del repositorio
    mock_repository.get_all_events.return_value = []
    mock_repository.create_event.return_value = Mock(id=1, title="Test Event")

    # Crear instancia del servicio
    event_service = EventService(mock_db)
    event_service.event_repository = mock_repository

    print("🧪 Testing Event Service Validations...")

    # Test 1: Evento válido
    print("\n1. Testing valid event creation...")
    valid_event_data = EventCreate(
        title="Valid Event",
        description="A valid event",
        location="Test Location",
        start_date=datetime.now() + timedelta(days=1),
        end_date=datetime.now() + timedelta(days=1, hours=2),
        capacity=100,
        is_active=True,
    )

    try:
        result = event_service.create_new_event(valid_event_data)
        print("✅ Valid event creation passed")
    except Exception as e:
        print(f"❌ Valid event creation failed: {e}")

    # Test 2: Fechas inválidas (end_date antes que start_date)
    print("\n2. Testing invalid dates (end before start)...")
    invalid_dates_event = EventCreate(
        title="Invalid Dates Event",
        description="Event with invalid dates",
        location="Test Location",
        start_date=datetime.now() + timedelta(days=2),
        end_date=datetime.now() + timedelta(days=1),  # End before start
        capacity=100,
        is_active=True,
    )

    try:
        event_service.create_new_event(invalid_dates_event)
        print("❌ Invalid dates test failed - should have raised error")
    except ValueError as e:
        if "End date must be after start date" in str(e):
            print("✅ Invalid dates validation passed")
        else:
            print(f"❌ Invalid dates validation failed: {e}")

    # Test 3: Capacidad negativa
    print("\n3. Testing negative capacity...")
    negative_capacity_event = EventCreate(
        title="Negative Capacity Event",
        description="Event with negative capacity",
        location="Test Location",
        start_date=datetime.now() + timedelta(days=1),
        end_date=datetime.now() + timedelta(days=1, hours=2),
        capacity=-10,  # Negative capacity
        is_active=True,
    )

    try:
        event_service.create_new_event(negative_capacity_event)
        print("❌ Negative capacity test failed - should have raised error")
    except ValueError as e:
        if "Capacity must be a positive number" in str(e):
            print("✅ Negative capacity validation passed")
        else:
            print(f"❌ Negative capacity validation failed: {e}")

    # Test 4: Título duplicado
    print("\n4. Testing duplicate title...")
    # Configurar el mock para simular un evento existente
    existing_event = Mock()
    existing_event.title = "Duplicate Title Event"
    mock_repository.get_all_events.return_value = [existing_event]

    duplicate_title_event = EventCreate(
        title="Duplicate Title Event",  # Same title as existing event
        description="Event with duplicate title",
        location="Different Location",
        start_date=datetime.now() + timedelta(days=2),
        end_date=datetime.now() + timedelta(days=2, hours=2),
        capacity=50,
        is_active=True,
    )

    try:
        event_service.create_new_event(duplicate_title_event)
        print("❌ Duplicate title test failed - should have raised error")
    except ValueError as e:
        if "Event already exists" in str(e):
            print("✅ Duplicate title validation passed")
        else:
            print(f"❌ Duplicate title validation failed: {e}")

    # Test 5: Fechas superpuestas
    print("\n5. Testing overlapping dates...")
    # Configurar el mock para simular un evento existente con fechas superpuestas
    overlapping_event = Mock()
    overlapping_event.title = "Existing Event"
    overlapping_event.start_date = datetime.now() + timedelta(days=1)
    overlapping_event.end_date = datetime.now() + timedelta(days=1, hours=2)
    mock_repository.get_all_events.return_value = [overlapping_event]

    overlapping_dates_event = EventCreate(
        title="Overlapping Event",
        description="Event with overlapping dates",
        location="Different Location",
        start_date=datetime.now() + timedelta(days=1),  # Same start time
        end_date=datetime.now() + timedelta(days=1, hours=2),  # Same end time
        capacity=50,
        is_active=True,
    )

    try:
        event_service.create_new_event(overlapping_dates_event)
        print("❌ Overlapping dates test failed - should have raised error")
    except ValueError as e:
        if "Event date already exists" in str(e):
            print("✅ Overlapping dates validation passed")
        else:
            print(f"❌ Overlapping dates validation failed: {e}")

    print("\n🎉 All validation tests completed!")


if __name__ == "__main__":
    test_validations()

