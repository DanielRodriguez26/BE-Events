from datetime import datetime
from typing import List, Optional

from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from app.api.schemas.event_registration_schemas import (
    EventRegistration, EventRegistrationCreate, EventRegistrationUpdate,
    EventRegistrationWithEvent)
from app.api.schemas.pagination_schema import Page
from app.db.models.event_models import Event
from app.db.models.event_register_models import \
    EventRegistration as EventRegistrationModel
from app.db.models.user_model import User
from app.infrastructure.repositories.event_registration_repository import EventRegistrationRepository


class EventRegistrationService:
    """Servicio para gestionar registros de usuarios a eventos"""

    def __init__(self, db: Session):
        self.event_registration_repository = EventRegistrationRepository(db)
        """Inicializa el servicio con la sesión de base de datos"""
        self.db = db

    def register_user_to_event(
        self, user_id: int, registration_data: EventRegistrationCreate
    ) -> EventRegistration:
        """
        Registra un usuario a un evento con validaciones de capacidad.

        Args:
            user_id: ID del usuario que se registra
            registration_data: Datos del registro

        Returns:
            EventRegistration: El registro creado

        Raises:
            ValueError: Si el evento no existe, no hay capacidad, o el usuario ya está registrado
        """
        # Verificar que el evento existe y está activo
        event = (
            self.db.query(Event)
            .filter(
                and_(Event.id == registration_data.event_id, Event.is_active == True)
            )
            .first()
        )

        if not event:
            raise ValueError("El evento no existe o no está activo")

        # Verificar que el usuario no esté ya registrado
        existing_registration = (
            self.db.query(EventRegistrationModel)
            .filter(
                and_(
                    EventRegistrationModel.event_id == registration_data.event_id,
                    EventRegistrationModel.user_id == user_id,
                )
            )
            .first()
        )

        if existing_registration:
            raise ValueError("Ya estás registrado en este evento")

        # Verificar capacidad disponible
        current_registrations = (
            self.db.query(func.sum(EventRegistrationModel.number_of_participants))
            .filter(EventRegistrationModel.event_id == registration_data.event_id)
            .scalar()
            or 0
        )

        available_capacity = event.capacity - current_registrations

        if available_capacity < registration_data.number_of_participants:
            raise ValueError(
                f"No hay suficiente capacidad. Disponible: {available_capacity}, "
                f"Solicitado: {registration_data.number_of_participants}"
            )

        # Crear el registro
        new_registration = EventRegistrationModel(
            event_id=registration_data.event_id,
            user_id=user_id,
            number_of_participants=registration_data.number_of_participants,
        )

        self.db.add(new_registration)
        self.db.commit()
        self.db.refresh(new_registration)

        return EventRegistration.from_orm(new_registration)

    def get_user_registrations(self, user_id: int, skip: int = 0, page: int = 1, limit: int = 20) -> Page[EventRegistrationWithEvent]:
        registrations = self.event_registration_repository.get_user_registrations(user_id, skip=skip, page=page, limit=limit)
        registration_list = [EventRegistrationWithEvent.model_validate(registration) for registration in registrations]
        total_registrations = self.event_registration_repository.get_count_registrations()
        total_pages = (total_registrations + limit - 1) // limit 

        return Page(
            items=registration_list,
            total_items=total_registrations,
            page=page,
            size=limit,
            total_pages=total_pages,
        )

    def get_event_registrations(
        self, event_id: int, skip: int = 0, page: int = 1, limit: int = 20
    ) -> Page[EventRegistration]:
        """
        Obtiene todos los registros de un evento específico.

        Args:
            event_id: ID del evento
            skip: Número de registros a saltar
            page: Número de página
            limit: Límite de registros por página

        Returns:
            Page[EventRegistration]: Página de registros
        """
        query = (
            self.db.query(EventRegistrationModel)
            .filter(EventRegistrationModel.event_id == event_id)
            .order_by(EventRegistrationModel.created_at.desc())
        )

        total = query.count()
        registrations = query.offset(skip).limit(limit).all()

        registration_schemas = [
            EventRegistration.from_orm(reg) for reg in registrations
        ]

        total_pages = (total + limit - 1) // limit

        return Page(
            items=registration_schemas,
            total_items=total,
            page=page,
            size=limit,
            total_pages=total_pages,
        )

    def update_registration(
        self, registration_id: int, user_id: int, update_data: EventRegistrationUpdate
    ) -> EventRegistration:
        """
        Actualiza un registro de evento.

        Args:
            registration_id: ID del registro
            user_id: ID del usuario (para verificar propiedad)
            update_data: Datos a actualizar

        Returns:
            EventRegistration: El registro actualizado

        Raises:
            ValueError: Si el registro no existe o no pertenece al usuario
        """
        registration = (
            self.db.query(EventRegistrationModel)
            .filter(
                and_(
                    EventRegistrationModel.id == registration_id,
                    EventRegistrationModel.user_id == user_id,
                )
            )
            .first()
        )

        if not registration:
            raise ValueError(
                "Registro no encontrado o no tienes permisos para modificarlo"
            )

        # Verificar capacidad disponible si se cambia el número de participantes
        if update_data.number_of_participants != registration.number_of_participants:
            event = (
                self.db.query(Event).filter(Event.id == registration.event_id).first()
            )

            current_registrations = (
                self.db.query(func.sum(EventRegistrationModel.number_of_participants))
                .filter(EventRegistrationModel.event_id == registration.event_id)
                .scalar()
                or 0
            )

            # Restar el registro actual para calcular la capacidad real disponible
            available_capacity = event.capacity - (
                current_registrations - registration.number_of_participants
            )

            if available_capacity < update_data.number_of_participants:
                raise ValueError(
                    f"No hay suficiente capacidad. Disponible: {available_capacity}, "
                    f"Solicitado: {update_data.number_of_participants}"
                )

        # Actualizar el registro
        setattr(
            registration, "number_of_participants", update_data.number_of_participants
        )
        setattr(registration, "updated_at", datetime.utcnow())

        self.db.commit()
        self.db.refresh(registration)

        return EventRegistration.from_orm(registration)

    def cancel_registration(self, registration_id: int, user_id: int) -> bool:
        """
        Cancela un registro de evento.

        Args:
            registration_id: ID del registro
            user_id: ID del usuario (para verificar propiedad)

        Returns:
            bool: True si se canceló exitosamente

        Raises:
            ValueError: Si el registro no existe o no pertenece al usuario
        """
        registration = (
            self.db.query(EventRegistrationModel)
            .filter(
                and_(
                    EventRegistrationModel.id == registration_id,
                    EventRegistrationModel.user_id == user_id,
                )
            )
            .first()
        )

        if not registration:
            raise ValueError(
                "Registro no encontrado o no tienes permisos para cancelarlo"
            )

        self.db.delete(registration)
        self.db.commit()

        return True

    def get_registration_by_id(
        self, registration_id: int
    ) -> Optional[EventRegistration]:
        """
        Obtiene un registro específico por ID.

        Args:
            registration_id: ID del registro

        Returns:
            EventRegistration: El registro encontrado o None
        """
        registration = (
            self.db.query(EventRegistrationModel)
            .filter(EventRegistrationModel.id == registration_id)
            .first()
        )

        if not registration:
            return None

        return EventRegistration.from_orm(registration)

    def get_event_capacity_info(self, event_id: int) -> dict:
        """
        Obtiene información de capacidad de un evento.

        Args:
            event_id: ID del evento

        Returns:
            dict: Información de capacidad
        """
        event = self.db.query(Event).filter(Event.id == event_id).first()

        if not event:
            raise ValueError("Evento no encontrado")

        total_registrations = (
            self.db.query(func.sum(EventRegistrationModel.number_of_participants))
            .filter(EventRegistrationModel.event_id == event_id)
            .scalar()
            or 0
        )

        return {
            "event_id": event_id,
            "total_capacity": event.capacity,
            "registered_participants": total_registrations,
            "available_capacity": event.capacity - total_registrations,
            "is_full": total_registrations >= event.capacity,
        }
