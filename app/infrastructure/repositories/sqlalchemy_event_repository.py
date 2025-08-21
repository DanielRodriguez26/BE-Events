import uuid
from typing import List, Optional

from sqlmodel import Session, select

from app.domain.entities.events import Event
from app.domain.repositories.events_repository import IEventsRepository
from app.infrastructure.database.base import engine
from app.infrastructure.database.model.event_model import EventModel


def map_model_to_domain(model: EventModel) -> Event:
    return Event(
        id=model.id,
        title=model.title,
        description=model.description,
        date=model.date,
        location=model.location,
        is_active=model.is_active,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


def map_domain_to_model(entity: Event) -> EventModel:
    return EventModel(
        id=entity.id,
        title=entity.title,
        description=entity.description,
        date=entity.date,
        location=entity.location,
        is_active=entity.is_active,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )


class SQLAlchemyEventsRepository(IEventsRepository):
    def __init__(self):
        self._engine = engine

    def get_all_events(self) -> List[Event]:
        with Session(self._engine) as session:
            results = session.exec(select(EventModel)).all()
            return [map_model_to_domain(m) for m in results]

    def get_event_by_id(self, event_id: uuid.UUID) -> Optional[Event]:
        with Session(self._engine) as session:
            model = session.get(EventModel, event_id)
            return map_model_to_domain(model) if model else None

    def create_event(self, event: Event) -> Event:
        with Session(self._engine) as session:
            model = map_domain_to_model(event)
            session.add(model)
            session.commit()
            session.refresh(model)
            return map_model_to_domain(model)

    def update_event(self, event: Event) -> Event:
        with Session(self._engine) as session:
            model = session.get(EventModel, event.id)
            if not model:
                raise ValueError("Event not found")
            model.title = event.title
            model.description = event.description
            model.date = event.date
            model.location = event.location
            model.is_active = event.is_active
            model.updated_at = event.updated_at
            session.add(model)
            session.commit()
            session.refresh(model)
            return map_model_to_domain(model)

    def delete_event(self, event_id: uuid.UUID) -> None:
        with Session(self._engine) as session:
            model = session.get(EventModel, event_id)
            if not model:
                raise ValueError("Event not found")
            session.delete(model)
            session.commit()

