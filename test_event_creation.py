from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

from app.db.base import engine
from app.db.models.event_models import Event
from app.api.schemas.event_schemas import EventCreate

# Crear una sesión de prueba
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

try:
    # Crear datos de prueba para un evento
    event_data = EventCreate(
        title="Evento de Prueba",
        description="Descripción del evento de prueba",
        location="Madrid, España",
        start_date=datetime.now() + timedelta(days=7),
        end_date=datetime.now() + timedelta(days=7, hours=3),
        capacity=100,
        is_active=True
    )
    
    print("Datos del evento a crear:")
    print(f"Title: {event_data.title}")
    print(f"Location: {event_data.location}")
    print(f"Capacity: {event_data.capacity}")
    
    # Crear el evento directamente en la base de datos
    db_event = Event(**event_data.model_dump())
    db.add(db_event)
    db.flush()
    db.refresh(db_event)
    db.commit()
    
    print(f"✅ Evento creado exitosamente con ID: {db_event.id}")
    
    # Verificar que el evento se creó correctamente
    created_event = db.query(Event).filter(Event.id == db_event.id).first()
    if created_event:
        print(f"✅ Evento verificado en la base de datos: {created_event.title}")
    else:
        print("❌ Error: El evento no se encontró en la base de datos")
        
except Exception as e:
    print(f"❌ Error al crear el evento: {e}")
    db.rollback()
finally:
    db.close()
