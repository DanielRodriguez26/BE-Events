#!/usr/bin/env python3
"""
Script para verificar que los datos semilla se insertaron correctamente.
"""

from sqlalchemy.orm import Session

from app.db.base import SessionLocal
from app.db.models import Event, EventRegistration, Role, User


def verify_seed_data():
    """Verify that seed data was created correctly."""
    db = SessionLocal()
    try:
        print("🔍 Verifying seed data...")

        # Check roles
        roles = db.query(Role).all()
        print(f"\n📋 Roles ({len(roles)}):")
        for role in roles:
            print(f"  - {role.name} (ID: {role.id})")

        # Check users
        users = db.query(User).all()
        print(f"\n👥 Users ({len(users)}):")
        for user in users:
            role = db.query(Role).filter(Role.id == user.role_id).first()
            print(
                f"  - {user.username} ({user.first_name} {user.last_name}) - Role: {role.name if role else 'Unknown'}"
            )

        # Check events
        events = db.query(Event).all()
        print(f"\n📅 Events ({len(events)}):")
        for event in events:
            status = "✅ Active" if event.is_active else "❌ Inactive"
            print(f"  - {event.title} - {status} - Capacity: {event.capacity}")
            print(f"    Location: {event.location}")
            print(
                f"    Date: {event.start_date.strftime('%Y-%m-%d %H:%M')} to {event.end_date.strftime('%Y-%m-%d %H:%M')}"
            )

        # Check registrations
        registrations = db.query(EventRegistration).all()
        print(f"\n🎫 Event Registrations ({len(registrations)}):")
        for reg in registrations:
            event = db.query(Event).filter(Event.id == reg.event_id).first()
            user = db.query(User).filter(User.id == reg.user_id).first()
            print(
                f"  - User: {user.username} registered for '{event.title}' ({reg.number_of_participants} participants)"
            )

        print(f"\n✅ Verification completed!")
        print(
            f"Total records: {len(roles) + len(users) + len(events) + len(registrations)}"
        )

    except Exception as e:
        print(f"❌ Error during verification: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    verify_seed_data()
