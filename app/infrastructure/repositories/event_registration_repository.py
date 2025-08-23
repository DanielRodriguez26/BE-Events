from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.models.event_register_models import (
    EventRegistration as EventRegistrationModel,
)


class EventRegistrationRepository:
    def __init__(self, db: Session):
        self.db = db
        self.event_registration_model = EventRegistrationModel

    def get_user_registrations (self, user_id: int, skip: int = 0, page: int = 1, limit: int = 20):
        return (
            self.db.query(self.event_registration_model)
            .filter(self.event_registration_model.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_all_event_registrations(self):
        return self.db.query(self.event_registration_model).all()

    def register_user_to_event(self, event_registration: EventRegistrationModel):
        self.db.add(event_registration)
        self.db.commit()
        self.db.refresh(event_registration)
        return event_registration

    def update_event_registration(self, event_registration: EventRegistrationModel):
        self.db.commit()
        self.db.refresh(event_registration)

    def get_count_registrations(self):
        return self.db.query(func.count(self.event_registration_model.id)).scalar() or 0
