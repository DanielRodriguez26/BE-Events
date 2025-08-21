from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.db.models import Event, EventRegistration, Role, User


def create_seed_data(db: Session):
    """Create seed data for the database."""

    # Create roles
    print("Creating roles...")
    admin_role = Role(name="admin")
    user_role = Role(name="user")
    organizer_role = Role(name="organizer")

    db.add_all([admin_role, user_role, organizer_role])
    db.commit()
    db.refresh(admin_role)
    db.refresh(user_role)
    db.refresh(organizer_role)

    # Create users
    print("Creating users...")
    admin_user = User(
        username="admin",
        first_name="Admin",
        last_name="User",
        phone="+1234567890",
        email="admin@example.com",
        password=get_password_hash("admin123"),
        is_active=True,
        role_id=admin_role.id,
    )

    organizer_user = User(
        username="organizer1",
        first_name="John",
        last_name="Organizer",
        phone="+1234567891",
        email="organizer@example.com",
        password=get_password_hash("organizer123"),
        is_active=True,
        role_id=organizer_role.id,
    )

    regular_user1 = User(
        username="user1",
        first_name="Alice",
        last_name="Smith",
        phone="+1234567892",
        email="alice@example.com",
        password=get_password_hash("user123"),
        is_active=True,
        role_id=user_role.id,
    )

    regular_user2 = User(
        username="user2",
        first_name="Bob",
        last_name="Johnson",
        phone="+1234567893",
        email="bob@example.com",
        password=get_password_hash("user123"),
        is_active=True,
        role_id=user_role.id,
    )

    db.add_all([admin_user, organizer_user, regular_user1, regular_user2])
    db.commit()
    db.refresh(admin_user)
    db.refresh(organizer_user)
    db.refresh(regular_user1)
    db.refresh(regular_user2)

    # Create events
    print("Creating events...")
    now = datetime.now()

    event1 = Event(
        title="Conferencia de Tecnología 2024",
        description="La conferencia más importante de tecnología del año. Reúne a expertos de la industria para discutir las últimas tendencias.",
        location="Centro de Convenciones Madrid",
        start_date=now + timedelta(days=30),
        end_date=now + timedelta(days=30, hours=8),
        capacity=500,
        is_active=True,
    )

    event2 = Event(
        title="Workshop de Python Avanzado",
        description="Aprende técnicas avanzadas de Python con expertos en el lenguaje.",
        location="Universidad Politécnica de Madrid",
        start_date=now + timedelta(days=15),
        end_date=now + timedelta(days=15, hours=6),
        capacity=50,
        is_active=True,
    )

    event3 = Event(
        title="Meetup de Desarrollo Web",
        description="Networking y charlas sobre desarrollo web moderno.",
        location="Coworking Space Barcelona",
        start_date=now + timedelta(days=7),
        end_date=now + timedelta(days=7, hours=3),
        capacity=100,
        is_active=True,
    )

    event4 = Event(
        title="Hackathon de IA",
        description="Competición de 48 horas para crear soluciones de IA innovadoras.",
        location="Tech Hub Valencia",
        start_date=now + timedelta(days=45),
        end_date=now + timedelta(days=47),
        capacity=200,
        is_active=True,
    )

    event5 = Event(
        title="Seminario de Marketing Digital",
        description="Estrategias efectivas de marketing digital para empresas.",
        location="Hotel Intercontinental Sevilla",
        start_date=now + timedelta(days=20),
        end_date=now + timedelta(days=20, hours=4),
        capacity=150,
        is_active=True,
    )

    # Evento inactivo para testing
    event6 = Event(
        title="Evento Cancelado",
        description="Este evento fue cancelado.",
        location="Lugar Cancelado",
        start_date=now + timedelta(days=10),
        end_date=now + timedelta(days=10, hours=2),
        capacity=50,
        is_active=False,
    )

    db.add_all([event1, event2, event3, event4, event5, event6])
    db.commit()
    db.refresh(event1)
    db.refresh(event2)
    db.refresh(event3)
    db.refresh(event4)
    db.refresh(event5)
    db.refresh(event6)

    # Create event registrations
    print("Creating event registrations...")

    registration1 = EventRegistration(
        event_id=event1.id, user_id=regular_user1.id, number_of_participants=2
    )

    registration2 = EventRegistration(
        event_id=event1.id, user_id=regular_user2.id, number_of_participants=1
    )

    registration3 = EventRegistration(
        event_id=event2.id, user_id=regular_user1.id, number_of_participants=1
    )

    registration4 = EventRegistration(
        event_id=event3.id, user_id=regular_user2.id, number_of_participants=3
    )

    registration5 = EventRegistration(
        event_id=event4.id, user_id=admin_user.id, number_of_participants=1
    )

    db.add_all(
        [registration1, registration2, registration3, registration4, registration5]
    )
    db.commit()

    print("Seed data created successfully!")
    print(f"Created {db.query(Role).count()} roles")
    print(f"Created {db.query(User).count()} users")
    print(f"Created {db.query(Event).count()} events")
    print(f"Created {db.query(EventRegistration).count()} event registrations")


def clear_seed_data(db: Session):
    """Clear all seed data from the database."""
    print("Clearing seed data...")

    # Delete in reverse order to respect foreign key constraints
    db.query(EventRegistration).delete()
    db.query(Event).delete()
    db.query(User).delete()
    db.query(Role).delete()

    db.commit()
    print("Seed data cleared successfully!")


if __name__ == "__main__":
    from app.db.base import SessionLocal

    db = SessionLocal()
    try:
        # Uncomment the line below to clear existing data
        # clear_seed_data(db)

        create_seed_data(db)
    finally:
        db.close()
