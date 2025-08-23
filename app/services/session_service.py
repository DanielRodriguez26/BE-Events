import math
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.infrastructure.repositories.session_repository import SessionRepository
from app.db.models import Session as SessionModel
from app.api.schemas.session_schemas import Session as SessionSchema, SessionCreate, SessionUpdate
from app.api.schemas.pagination_schema import Page


class SessionService:
    def __init__(self, db: Session):
        self.db = db
        self.session_repository = SessionRepository(db)

    def get_all_sessions(self, skip: int = 0, page: int = 1, limit: int = 100) -> Page[SessionSchema]:
        sessions = self.session_repository.get_all_sessions(skip=skip, limit=limit)
        session_list = [SessionSchema.model_validate(session) for session in sessions]
        total_sessions = self.session_repository.get_sessions_count()
        total_pages = math.ceil(total_sessions / limit) if total_sessions > 0 else 1
        return Page(
            items=session_list,
            page=page,
            size=limit,
            total_items=total_sessions,
            total_pages=total_pages
        )

    def get_sessions_by_event(self, event_id: int, skip: int = 0, page: int = 1, limit: int = 100) -> Page[SessionSchema]:
        sessions = self.session_repository.get_sessions_by_event(event_id, skip=skip, limit=limit)
        session_list = [SessionSchema.model_validate(session) for session in sessions]
        total_sessions = self.session_repository.get_sessions_count_by_event(event_id)
        total_pages = math.ceil(total_sessions / limit) if total_sessions > 0 else 1
        return Page(
            items=session_list,
            page=page,
            size=limit,
            total_items=total_sessions,
            total_pages=total_pages
        )

    def get_session_by_id(self, session_id: int) -> Optional[SessionSchema]:
        session = self.session_repository.get_session_by_id(session_id)
        if session:
            return SessionSchema.model_validate(session)
        return None
    
    def create_session(self, session_data: SessionCreate) -> SessionSchema:
        # Validación 1: Verificar que el evento existe
        event = self.session_repository.get_event_by_id(session_data.event_id)
        if not event:
            raise ValueError(f"Event with id {session_data.event_id} does not exist")
        
        # Validación 2: Verificar que el speaker existe (si se proporciona)
        if session_data.speaker_id:
            speaker = self.session_repository.get_speaker_by_id(session_data.speaker_id)
            if not speaker:
                raise ValueError(f"Speaker with id {session_data.speaker_id} does not exist")
        
        # Validación 3: Verificar que el horario está dentro del rango del evento
        if session_data.start_time < event.start_date or session_data.end_time > event.end_date:
            raise ValueError("Session schedule must be within the event's date range")
        
        # Validación 4: Verificar que no hay conflictos de horario
        conflicts = self.session_repository.check_schedule_conflicts(
            session_data.event_id, 
            session_data.start_time, 
            session_data.end_time
        )
        if conflicts:
            conflict_titles = [f"'{c.title}' ({c.start_time.strftime('%H:%M')}-{c.end_time.strftime('%H:%M')})" for c in conflicts]
            raise ValueError(f"Schedule conflict with existing sessions: {', '.join(conflict_titles)}")
        
        # Validación 5: Verificar capacidad positiva si se proporciona
        if session_data.capacity is not None and session_data.capacity <= 0:
            raise ValueError("Capacity must be a positive number")
        
        # Crear la sesión
        session_model = SessionModel(**session_data.model_dump())
        created_session = self.session_repository.create_session(session_model)
        return SessionSchema.model_validate(created_session)
    
    def update_session(self, session_id: int, session_data: SessionUpdate) -> Optional[SessionSchema]:
        # Verificar que la sesión existe
        existing_session = self.session_repository.get_session_by_id(session_id)
        if not existing_session:
            return None
        
        # Obtener el evento para validaciones
        event = self.session_repository.get_event_by_id(existing_session.event_id)
        if not event:
            raise ValueError(f"Event with id {existing_session.event_id} does not exist")
        
        # Preparar datos para actualización
        update_data = session_data.model_dump(exclude_unset=True)
        
        # Validación 1: Verificar que el speaker existe (si se proporciona)
        if session_data.speaker_id is not None:
            speaker = self.session_repository.get_speaker_by_id(session_data.speaker_id)
            if not speaker:
                raise ValueError(f"Speaker with id {session_data.speaker_id} does not exist")
        
        # Validación 2: Verificar horarios si se actualizan
        start_time = update_data.get('start_time', existing_session.start_time)
        end_time = update_data.get('end_time', existing_session.end_time)
        
        # Validación 3: Verificar que el horario está dentro del rango del evento
        if start_time < event.start_date or end_time > event.end_date:
            raise ValueError("Session schedule must be within the event's date range")
        
        # Validación 4: Verificar que no hay conflictos de horario
        conflicts = self.session_repository.check_schedule_conflicts(
            existing_session.event_id, 
            start_time, 
            end_time,
            exclude_session_id=session_id
        )
        if conflicts:
            conflict_titles = [f"'{c.title}' ({c.start_time.strftime('%H:%M')}-{c.end_time.strftime('%H:%M')})" for c in conflicts]
            raise ValueError(f"Schedule conflict with existing sessions: {', '.join(conflict_titles)}")
        
        # Validación 5: Verificar capacidad positiva si se proporciona
        if session_data.capacity is not None and session_data.capacity <= 0:
            raise ValueError("Capacity must be a positive number")
        
        # Actualizar la sesión
        updated_session = self.session_repository.update_session(session_id, update_data)
        if updated_session:
            return SessionSchema.model_validate(updated_session)
        return None
    
    def delete_session(self, session_id: int) -> bool:
        return self.session_repository.delete_session(session_id)

