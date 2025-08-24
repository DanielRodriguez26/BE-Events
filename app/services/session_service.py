import math
from typing import List, Optional
from datetime import datetime, timedelta
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

    def _validate_session_schedule(self, session_data: SessionCreate, event_start: datetime, event_end: datetime) -> None:
        """Validaciones adicionales de horarios para sesiones"""
        
        # Validación 1: Verificar que el evento existe
        if not event_start or not event_end:
            raise ValueError("Event dates are required")
        
        # Validación 2: Verificar que el horario está dentro del rango del evento
        if session_data.start_time < event_start or session_data.end_time > event_end:
            raise ValueError("Session schedule must be within the event's date range")
        
        # Validación 3: Verificar que la sesión no empiece antes del evento
        if session_data.start_time < event_start:
            raise ValueError("Session cannot start before the event")
        
        # Validación 4: Verificar que la sesión no termine después del evento
        if session_data.end_time > event_end:
            raise ValueError("Session cannot end after the event")
        
        # Validación 5: Verificar que no hay sesiones en horarios no laborables (opcional)
        # Solo permitir sesiones entre 8:00 AM y 10:00 PM
        start_hour = session_data.start_time.hour
        end_hour = session_data.end_time.hour
        
        if start_hour < 8 or end_hour > 22:
            raise ValueError("Sessions can only be scheduled between 8:00 AM and 10:00 PM")
        
        # Validación 6: Verificar que no hay sesiones que crucen la medianoche
        if session_data.start_time.date() != session_data.end_time.date():
            raise ValueError("Sessions cannot span across midnight")
        
        # Validación 7: Verificar que hay tiempo suficiente entre sesiones (mínimo 15 minutos)
        # Esta validación se hace en check_schedule_conflicts_with_buffer

    def _check_schedule_conflicts_with_buffer(self, event_id: int, start_time: datetime, end_time: datetime, 
                                            exclude_session_id: Optional[int] = None, buffer_minutes: int = 15) -> List[SessionModel]:
        """Verificar conflictos de horario incluyendo un buffer entre sesiones"""
        buffer_time = timedelta(minutes=buffer_minutes)
        
        # Obtener todas las sesiones del evento
        all_sessions = self.session_repository.get_sessions_by_event(event_id, skip=0, limit=1000)
        
        conflicts = []
        for session in all_sessions:
            if exclude_session_id and session.id == exclude_session_id:
                continue
                
            # Verificar si hay solapamiento incluyendo el buffer
            session_start_with_buffer = session.start_time - buffer_time
            session_end_with_buffer = session.end_time + buffer_time
            
            # Verificar si hay conflicto
            if (start_time < session_end_with_buffer and end_time > session_start_with_buffer):
                conflicts.append(session)
        
        return conflicts

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
        
        # Validación 3: Validaciones adicionales de horarios
        self._validate_session_schedule(session_data, event.start_date, event.end_date)#type: ignore
        
        # Validación 4: Verificar que no hay conflictos de horario con buffer
        conflicts = self._check_schedule_conflicts_with_buffer(
            session_data.event_id, 
            session_data.start_time, 
            session_data.end_time
        )
        if conflicts:
            conflict_titles = [f"'{c.title}' ({c.start_time.strftime('%H:%M')}-{c.end_time.strftime('%H:%M')})" for c in conflicts]
            raise ValueError(f"Schedule conflict with existing sessions (including 15-minute buffer): {', '.join(conflict_titles)}")
        
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
        event = self.session_repository.get_event_by_id(int(existing_session.event_id))
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
        
        # Validación 3: Validaciones adicionales de horarios si se actualizan
        if 'start_time' in update_data or 'end_time' in update_data:
            # Crear un objeto temporal para validaciones
            temp_session_data = SessionCreate(
                title=str(existing_session.title),
                event_id=int(existing_session.event_id),
                start_time=start_time,
                end_time=end_time,
                speaker_id=session_data.speaker_id,
                capacity=session_data.capacity
            )
            self._validate_session_schedule(temp_session_data, event.start_date, event.end_date) #type: ignore
        
        # Validación 4: Verificar que no hay conflictos de horario con buffer
        conflicts = self._check_schedule_conflicts_with_buffer(
            int(existing_session.event_id), 
            start_time, 
            end_time,
            exclude_session_id=session_id
        )
        if conflicts:
            conflict_titles = [f"'{c.title}' ({c.start_time.strftime('%H:%M')}-{c.end_time.strftime('%H:%M')})" for c in conflicts]
            raise ValueError(f"Schedule conflict with existing sessions (including 15-minute buffer): {', '.join(conflict_titles)}")
        
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

