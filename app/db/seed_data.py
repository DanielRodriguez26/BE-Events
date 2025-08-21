"""
Seed data for the Events API database.

This module provides functions to populate the database with initial data
for development and testing purposes.
"""

from datetime import datetime, timedelta
from typing import List

from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.db.models import Event, EventRegistration, Role
from app.db.models import Session as EventSession
from app.db.models import Speaker, User


def create_seed_data(db: Session):
    """Create comprehensive seed data for the database."""

    print("🌱 Starting database seeding...")

    # Create roles
    print("📋 Creating roles...")
    roles = create_roles(db)

    # Create users
    print("👥 Creating users...")
    users = create_users(db, roles)

    # Create speakers
    print("🎤 Creating speakers...")
    speakers = create_speakers(db)

    # Create events
    print("🎉 Creating events...")
    events = create_events(db)

    # Create sessions
    print("📅 Creating sessions...")
    create_sessions(db, events, speakers)

    # Create event registrations
    print("📝 Creating event registrations...")
    create_event_registrations(db, events, users)

    print("✅ Seed data created successfully!")
    print_summary(db)


def create_roles(db: Session) -> dict:
    """Create and return roles dictionary."""
    roles_data = [
        {"name": "admin", "description": "Administrator with full access"},
        {
            "name": "organizer",
            "description": "Event organizer with event management permissions",
        },
        {"name": "user", "description": "Regular user with basic permissions"},
        {
            "name": "moderator",
            "description": "Moderator with content management permissions",
        },
    ]

    roles = {}
    for role_data in roles_data:
        role = Role(name=role_data["name"])
        db.add(role)
        db.commit()
        db.refresh(role)
        roles[role_data["name"]] = role

    return roles


def create_users(db: Session, roles: dict) -> dict:
    """Create and return users dictionary."""
    users_data = [
        {
            "username": "admin",
            "first_name": "Admin",
            "last_name": "User",
            "phone": "+34 600 000 001",
            "email": "admin@eventsapi.com",
            "password": "admin123",
            "role": "admin",
            "is_active": True,
        },
        {
            "username": "organizer1",
            "first_name": "María",
            "last_name": "García",
            "phone": "+34 600 000 002",
            "email": "maria.garcia@eventsapi.com",
            "password": "organizer123",
            "role": "organizer",
            "is_active": True,
        },
        {
            "username": "organizer2",
            "first_name": "Carlos",
            "last_name": "López",
            "phone": "+34 600 000 003",
            "email": "carlos.lopez@eventsapi.com",
            "password": "organizer123",
            "role": "organizer",
            "is_active": True,
        },
        {
            "username": "moderator1",
            "first_name": "Ana",
            "last_name": "Martínez",
            "phone": "+34 600 000 004",
            "email": "ana.martinez@eventsapi.com",
            "password": "moderator123",
            "role": "moderator",
            "is_active": True,
        },
        {
            "username": "user1",
            "first_name": "Luis",
            "last_name": "Rodríguez",
            "phone": "+34 600 000 005",
            "email": "luis.rodriguez@example.com",
            "password": "user123",
            "role": "user",
            "is_active": True,
        },
        {
            "username": "user2",
            "first_name": "Sofia",
            "last_name": "Fernández",
            "phone": "+34 600 000 006",
            "email": "sofia.fernandez@example.com",
            "password": "user123",
            "role": "user",
            "is_active": True,
        },
        {
            "username": "user3",
            "first_name": "David",
            "last_name": "Pérez",
            "phone": "+34 600 000 007",
            "email": "david.perez@example.com",
            "password": "user123",
            "role": "user",
            "is_active": True,
        },
        {
            "username": "user4",
            "first_name": "Elena",
            "last_name": "González",
            "phone": "+34 600 000 008",
            "email": "elena.gonzalez@example.com",
            "password": "user123",
            "role": "user",
            "is_active": True,
        },
        {
            "username": "inactive_user",
            "first_name": "Inactive",
            "last_name": "User",
            "phone": "+34 600 000 009",
            "email": "inactive@example.com",
            "password": "user123",
            "role": "user",
            "is_active": False,
        },
    ]

    users = {}
    for user_data in users_data:
        user = User(
            username=user_data["username"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            phone=user_data["phone"],
            email=user_data["email"],
            password=get_password_hash(user_data["password"]),
            is_active=user_data["is_active"],
            role_id=roles[user_data["role"]].id,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        users[user_data["username"]] = user

    return users


def create_speakers(db: Session) -> dict:
    """Create and return speakers dictionary."""
    speakers_data = [
        {
            "name": "Dr. María González",
            "bio": "Experta en Inteligencia Artificial con más de 15 años de experiencia en investigación y desarrollo de sistemas de IA.",
            "email": "maria.gonzalez@ai-expert.com",
            "phone": "+34 600 000 101",
            "company": "AI Research Institute",
            "is_active": True,
        },
        {
            "name": "Carlos Rodríguez",
            "bio": "Desarrollador senior de Python con experiencia en frameworks como Django, FastAPI y Flask.",
            "email": "carlos.rodriguez@python-dev.com",
            "phone": "+34 600 000 102",
            "company": "TechCorp Solutions",
            "is_active": True,
        },
        {
            "name": "Ana Martínez",
            "bio": "Especialista en ciberseguridad con certificaciones en CISSP y CEH. Experta en análisis de amenazas.",
            "email": "ana.martinez@cyber-security.com",
            "phone": "+34 600 000 103",
            "company": "SecureNet Consulting",
            "is_active": True,
        },
        {
            "name": "Luis Fernández",
            "bio": "Arquitecto de software con experiencia en microservicios y sistemas distribuidos.",
            "email": "luis.fernandez@software-arch.com",
            "phone": "+34 600 000 104",
            "company": "CloudTech Solutions",
            "is_active": True,
        },
        {
            "name": "Sofia Pérez",
            "bio": "Experta en DevOps y automatización con experiencia en Docker, Kubernetes y CI/CD.",
            "email": "sofia.perez@devops-expert.com",
            "phone": "+34 600 000 105",
            "company": "DevOps Masters",
            "is_active": True,
        },
        {
            "name": "David López",
            "bio": "Especialista en blockchain y fintech con experiencia en desarrollo de smart contracts.",
            "email": "david.lopez@blockchain-dev.com",
            "phone": "+34 600 000 106",
            "company": "Blockchain Innovations",
            "is_active": True,
        },
        {
            "name": "Elena García",
            "bio": "Desarrolladora frontend especializada en React, Vue.js y tecnologías modernas de UI/UX.",
            "email": "elena.garcia@frontend-dev.com",
            "phone": "+34 600 000 107",
            "company": "WebDesign Studio",
            "is_active": True,
        },
        {
            "name": "Roberto Silva",
            "bio": "Experto en machine learning y data science con experiencia en proyectos de big data.",
            "email": "roberto.silva@ml-expert.com",
            "phone": "+34 600 000 108",
            "company": "DataScience Labs",
            "is_active": True,
        },
    ]

    speakers = {}
    for speaker_data in speakers_data:
        speaker = Speaker(**speaker_data)
        db.add(speaker)
        db.commit()
        db.refresh(speaker)
        speakers[speaker_data["name"]] = speaker

    return speakers


def create_events(db: Session) -> List[Event]:
    """Create and return list of events."""
    now = datetime.now()

    events_data = [
        {
            "title": "Conferencia de Tecnología 2024",
            "description": "La conferencia más importante de tecnología del año. Reúne a expertos de la industria para discutir las últimas tendencias en IA, blockchain, y desarrollo sostenible.",
            "location": "Centro de Convenciones Madrid",
            "start_date": now + timedelta(days=30),
            "end_date": now + timedelta(days=30, hours=8),
            "capacity": 500,
            "is_active": True,
        },
        {
            "title": "Workshop de Python Avanzado",
            "description": "Aprende técnicas avanzadas de Python con expertos en el lenguaje. Incluye asyncio, decoradores, metaclasses y optimización de rendimiento.",
            "location": "Universidad Politécnica de Madrid",
            "start_date": now + timedelta(days=15),
            "end_date": now + timedelta(days=15, hours=6),
            "capacity": 50,
            "is_active": True,
        },
        {
            "title": "Meetup de Desarrollo Web",
            "description": "Networking y charlas sobre desarrollo web moderno. React, Vue.js, y las últimas tendencias en frontend y backend.",
            "location": "Coworking Space Barcelona",
            "start_date": now + timedelta(days=7),
            "end_date": now + timedelta(days=7, hours=3),
            "capacity": 100,
            "is_active": True,
        },
        {
            "title": "Hackathon de Inteligencia Artificial",
            "description": "Competición de 48 horas para crear soluciones de IA innovadoras. Premios en efectivo y oportunidades de networking con empresas líderes.",
            "location": "Tech Hub Valencia",
            "start_date": now + timedelta(days=45),
            "end_date": now + timedelta(days=47),
            "capacity": 200,
            "is_active": True,
        },
        {
            "title": "Seminario de Marketing Digital",
            "description": "Estrategias efectivas de marketing digital para empresas. SEO, SEM, redes sociales y análisis de datos.",
            "location": "Hotel Intercontinental Sevilla",
            "start_date": now + timedelta(days=20),
            "end_date": now + timedelta(days=20, hours=4),
            "capacity": 150,
            "is_active": True,
        },
        {
            "title": "Conferencia de Ciberseguridad",
            "description": "Últimas amenazas y soluciones en ciberseguridad. Expertos internacionales comparten sus experiencias y mejores prácticas.",
            "location": "Palacio de Congresos de Málaga",
            "start_date": now + timedelta(days=60),
            "end_date": now + timedelta(days=60, hours=6),
            "capacity": 300,
            "is_active": True,
        },
        {
            "title": "Workshop de Machine Learning",
            "description": "Introducción práctica al machine learning con Python. Desde conceptos básicos hasta implementación de modelos reales.",
            "location": "Escuela de Ingeniería de Bilbao",
            "start_date": now + timedelta(days=25),
            "end_date": now + timedelta(days=25, hours=5),
            "capacity": 75,
            "is_active": True,
        },
        {
            "title": "Meetup de DevOps",
            "description": "Docker, Kubernetes, CI/CD y automatización. Comparte experiencias y aprende de expertos en DevOps.",
            "location": "Impact Hub Madrid",
            "start_date": now + timedelta(days=12),
            "end_date": now + timedelta(days=12, hours=2),
            "capacity": 80,
            "is_active": True,
        },
        {
            "title": "Conferencia de Blockchain",
            "description": "El futuro de las finanzas descentralizadas. DeFi, NFTs, y aplicaciones empresariales de blockchain.",
            "location": "Centro de Innovación de Barcelona",
            "start_date": now + timedelta(days=40),
            "end_date": now + timedelta(days=40, hours=7),
            "capacity": 250,
            "is_active": True,
        },
        {
            "title": "Workshop de React Native",
            "description": "Desarrollo de aplicaciones móviles multiplataforma con React Native. Desde configuración hasta publicación.",
            "location": "Campus de Google Madrid",
            "start_date": now + timedelta(days=18),
            "end_date": now + timedelta(days=18, hours=4),
            "capacity": 60,
            "is_active": True,
        },
        {
            "title": "Evento Cancelado - Mantenimiento",
            "description": "Este evento fue cancelado debido a trabajos de mantenimiento en las instalaciones.",
            "location": "Lugar Cancelado",
            "start_date": now + timedelta(days=10),
            "end_date": now + timedelta(days=10, hours=2),
            "capacity": 50,
            "is_active": False,
        },
        {
            "title": "Evento Pasado - Conferencia de 2023",
            "description": "Este es un evento que ya pasó, para testing de filtros por fecha.",
            "location": "Centro Histórico",
            "start_date": now - timedelta(days=30),
            "end_date": now - timedelta(days=30, hours=3),
            "capacity": 100,
            "is_active": False,
        },
    ]

    events = []
    for event_data in events_data:
        event = Event(**event_data)
        db.add(event)
        db.commit()
        db.refresh(event)
        events.append(event)

    return events


def create_sessions(db: Session, events: List[Event], speakers: dict):
    """Create sessions for events."""
    sessions_data = [
        # Conferencia de Tecnología 2024
        {
            "title": "El Futuro de la IA en 2024",
            "description": "Tendencias emergentes en inteligencia artificial y su impacto en la industria.",
            "start_time": events[0].start_date + timedelta(hours=1),
            "end_time": events[0].start_date + timedelta(hours=2),
            "event": events[0],
            "speaker": speakers["Dr. María González"],
            "is_active": True,
        },
        {
            "title": "Blockchain y DeFi: Revolución Financiera",
            "description": "Cómo las finanzas descentralizadas están transformando el mundo financiero.",
            "start_time": events[0].start_date + timedelta(hours=3),
            "end_time": events[0].start_date + timedelta(hours=4),
            "event": events[0],
            "speaker": speakers["David López"],
            "is_active": True,
        },
        # Workshop de Python Avanzado
        {
            "title": "Asyncio y Programación Asíncrona",
            "description": "Aprende a escribir código Python asíncrono eficiente y escalable.",
            "start_time": events[1].start_date + timedelta(hours=1),
            "end_time": events[1].start_date + timedelta(hours=2),
            "event": events[1],
            "speaker": speakers["Carlos Rodríguez"],
            "is_active": True,
        },
        {
            "title": "Decoradores y Metaclasses",
            "description": "Técnicas avanzadas de metaprogramación en Python.",
            "start_time": events[1].start_date + timedelta(hours=3),
            "end_time": events[1].start_date + timedelta(hours=4),
            "event": events[1],
            "speaker": speakers["Carlos Rodríguez"],
            "is_active": True,
        },
        # Conferencia de Ciberseguridad
        {
            "title": "Amenazas Cibernéticas Emergentes",
            "description": "Nuevas técnicas de ataque y estrategias de defensa.",
            "start_time": events[5].start_date + timedelta(hours=1),
            "end_time": events[5].start_date + timedelta(hours=2),
            "event": events[5],
            "speaker": speakers["Ana Martínez"],
            "is_active": True,
        },
        {
            "title": "Análisis Forense Digital",
            "description": "Técnicas de investigación y análisis de incidentes de seguridad.",
            "start_time": events[5].start_date + timedelta(hours=3),
            "end_time": events[5].start_date + timedelta(hours=4),
            "event": events[5],
            "speaker": speakers["Ana Martínez"],
            "is_active": True,
        },
        # Workshop de Machine Learning
        {
            "title": "Introducción al Machine Learning",
            "description": "Conceptos básicos y primeros pasos en ML.",
            "start_time": events[6].start_date + timedelta(hours=1),
            "end_time": events[6].start_date + timedelta(hours=2),
            "event": events[6],
            "speaker": speakers["Roberto Silva"],
            "is_active": True,
        },
        {
            "title": "Implementación de Modelos en Producción",
            "description": "Cómo desplegar y mantener modelos de ML en entornos reales.",
            "start_time": events[6].start_date + timedelta(hours=3),
            "end_time": events[6].start_date + timedelta(hours=4),
            "event": events[6],
            "speaker": speakers["Roberto Silva"],
            "is_active": True,
        },
        # Meetup de DevOps
        {
            "title": "Docker y Contenedores",
            "description": "Fundamentos de contenerización y mejores prácticas.",
            "start_time": events[7].start_date + timedelta(hours=0.5),
            "end_time": events[7].start_date + timedelta(hours=1.5),
            "event": events[7],
            "speaker": speakers["Sofia Pérez"],
            "is_active": True,
        },
        # Conferencia de Blockchain
        {
            "title": "Smart Contracts y DeFi",
            "description": "Desarrollo de contratos inteligentes y aplicaciones DeFi.",
            "start_time": events[8].start_date + timedelta(hours=1),
            "end_time": events[8].start_date + timedelta(hours=2),
            "event": events[8],
            "speaker": speakers["David López"],
            "is_active": True,
        },
        {
            "title": "NFTs y Metaverso",
            "description": "El futuro de los tokens no fungibles y el metaverso.",
            "start_time": events[8].start_date + timedelta(hours=3),
            "end_time": events[8].start_date + timedelta(hours=4),
            "event": events[8],
            "speaker": speakers["David López"],
            "is_active": True,
        },
    ]

    for session_data in sessions_data:
        session = EventSession(
            title=session_data["title"],
            description=session_data["description"],
            start_time=session_data["start_time"],
            end_time=session_data["end_time"],
            event_id=session_data["event"].id,
            speaker_id=session_data["speaker"].id,
            is_active=session_data["is_active"],
        )
        db.add(session)

    db.commit()


def create_event_registrations(db: Session, events: List[Event], users: dict):
    """Create event registrations."""
    registrations_data = [
        # Conferencia de Tecnología 2024
        {"event": events[0], "user": users["user1"], "participants": 2},
        {"event": events[0], "user": users["user2"], "participants": 1},
        {"event": events[0], "user": users["user3"], "participants": 3},
        {"event": events[0], "user": users["user4"], "participants": 1},
        # Workshop de Python Avanzado
        {"event": events[1], "user": users["user1"], "participants": 1},
        {"event": events[1], "user": users["user2"], "participants": 1},
        {"event": events[1], "user": users["admin"], "participants": 1},
        # Meetup de Desarrollo Web
        {"event": events[2], "user": users["user3"], "participants": 2},
        {"event": events[2], "user": users["user4"], "participants": 1},
        {"event": events[2], "user": users["organizer1"], "participants": 1},
        # Hackathon de IA
        {"event": events[3], "user": users["admin"], "participants": 1},
        {"event": events[3], "user": users["user1"], "participants": 1},
        {"event": events[3], "user": users["user2"], "participants": 2},
        {"event": events[3], "user": users["moderator1"], "participants": 1},
        # Seminario de Marketing Digital
        {"event": events[4], "user": users["organizer2"], "participants": 1},
        {"event": events[4], "user": users["user3"], "participants": 1},
        {"event": events[4], "user": users["user4"], "participants": 2},
        # Conferencia de Ciberseguridad
        {"event": events[5], "user": users["admin"], "participants": 1},
        {"event": events[5], "user": users["user1"], "participants": 1},
        # Workshop de Machine Learning
        {"event": events[6], "user": users["user2"], "participants": 1},
        {"event": events[6], "user": users["user3"], "participants": 1},
        # Meetup de DevOps
        {"event": events[7], "user": users["user4"], "participants": 1},
        {"event": events[7], "user": users["organizer1"], "participants": 1},
        # Conferencia de Blockchain
        {"event": events[8], "user": users["admin"], "participants": 1},
        {"event": events[8], "user": users["user1"], "participants": 2},
        {"event": events[8], "user": users["user2"], "participants": 1},
        # Workshop de React Native
        {"event": events[9], "user": users["user3"], "participants": 1},
        {"event": events[9], "user": users["user4"], "participants": 1},
    ]

    for reg_data in registrations_data:
        registration = EventRegistration(
            event_id=reg_data["event"].id,
            user_id=reg_data["user"].id,
            number_of_participants=reg_data["participants"],
        )
        db.add(registration)

    db.commit()


def print_summary(db: Session):
    """Print a summary of created data."""
    print("\n📊 Database Summary:")
    print(f"   👥 Users: {db.query(User).count()}")
    print(f"   📋 Roles: {db.query(Role).count()}")
    print(f"   🎤 Speakers: {db.query(Speaker).count()}")
    print(f"   🎉 Events: {db.query(Event).count()}")
    print(f"   📅 Sessions: {db.query(EventSession).count()}")
    print(f"   📝 Registrations: {db.query(EventRegistration).count()}")

    # Print some statistics
    active_events = db.query(Event).filter(Event.is_active == True).count()
    inactive_events = db.query(Event).filter(Event.is_active == False).count()
    active_users = db.query(User).filter(User.is_active == True).count()
    inactive_users = db.query(User).filter(User.is_active == False).count()
    active_speakers = db.query(Speaker).filter(Speaker.is_active == True).count()
    active_sessions = (
        db.query(EventSession).filter(EventSession.is_active == True).count()
    )

    print(f"\n📈 Statistics:")
    print(f"   ✅ Active Events: {active_events}")
    print(f"   ❌ Inactive Events: {inactive_events}")
    print(f"   ✅ Active Users: {active_users}")
    print(f"   ❌ Inactive Users: {inactive_users}")
    print(f"   ✅ Active Speakers: {active_speakers}")
    print(f"   ✅ Active Sessions: {active_sessions}")

    # Print upcoming events
    upcoming_events = (
        db.query(Event)
        .filter(Event.start_date > datetime.now(), Event.is_active == True)
        .count()
    )

    print(f"   🔮 Upcoming Events: {upcoming_events}")

    # Print role distribution
    print(f"\n👥 Role Distribution:")
    for role in db.query(Role).all():
        user_count = db.query(User).filter(User.role_id == role.id).count()
        print(f"   {role.name.capitalize()}: {user_count} users")


def clear_seed_data(db: Session):
    """Clear all seed data from the database."""
    print("🗑️ Clearing seed data...")

    # Delete in reverse order to respect foreign key constraints
    db.query(EventRegistration).delete()
    db.query(EventSession).delete()
    db.query(Event).delete()
    db.query(Speaker).delete()
    db.query(User).delete()
    db.query(Role).delete()

    db.commit()
    print("✅ Seed data cleared successfully!")


def reset_database(db: Session):
    """Reset the database by clearing and recreating seed data."""
    print("🔄 Resetting database...")
    clear_seed_data(db)
    create_seed_data(db)
    print("✅ Database reset completed!")


def verify_seed_data(db: Session):
    """Verify that seed data was created correctly."""
    print("🔍 Verifying seed data...")

    # Check counts
    role_count = db.query(Role).count()
    user_count = db.query(User).count()
    speaker_count = db.query(Speaker).count()
    event_count = db.query(Event).count()
    session_count = db.query(EventSession).count()
    registration_count = db.query(EventRegistration).count()

    print(f"   📋 Roles: {role_count}")
    print(f"   👥 Users: {user_count}")
    print(f"   🎤 Speakers: {speaker_count}")
    print(f"   🎉 Events: {event_count}")
    print(f"   📅 Sessions: {session_count}")
    print(f"   📝 Registrations: {registration_count}")

    # Check relationships
    print("\n🔗 Checking relationships...")

    # Check user-role relationships
    for user in db.query(User).all():
        role = db.query(Role).filter(Role.id == user.role_id).first()
        if not role:
            print(f"   ❌ User {user.username} has invalid role_id: {user.role_id}")
        else:
            print(f"   ✅ User {user.username} -> Role {role.name}")

    # Check session relationships
    for session in db.query(EventSession).all():
        event = db.query(Event).filter(Event.id == session.event_id).first()
        speaker = db.query(Speaker).filter(Speaker.id == session.speaker_id).first()

        if not event:
            print(
                f"   ❌ Session {session.id} has invalid event_id: {session.event_id}"
            )
        elif not speaker:
            print(
                f"   ❌ Session {session.id} has invalid speaker_id: {session.speaker_id}"
            )
        else:
            print(f"   ✅ Session {session.id}: {speaker.name} -> {event.title}")

    # Check registration relationships
    for reg in db.query(EventRegistration).all():
        event = db.query(Event).filter(Event.id == reg.event_id).first()
        user = db.query(User).filter(User.id == reg.user_id).first()

        if not event:
            print(f"   ❌ Registration {reg.id} has invalid event_id: {reg.event_id}")
        elif not user:
            print(f"   ❌ Registration {reg.id} has invalid user_id: {reg.user_id}")
        else:
            print(f"   ✅ Registration {reg.id}: {user.username} -> {event.title}")

    print("✅ Verification completed!")


if __name__ == "__main__":
    from app.db.base import SessionLocal

    db = SessionLocal()
    try:
        # Choose one of the following options:

        # Option 1: Create seed data (keeps existing data)
        create_seed_data(db)

        # Option 2: Clear existing data and create new seed data
        # reset_database(db)

        # Option 3: Only clear data
        # clear_seed_data(db)

        # Option 4: Verify existing data
        # verify_seed_data(db)

    finally:
        db.close()
