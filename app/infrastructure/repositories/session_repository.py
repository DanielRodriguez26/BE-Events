from datetime import datetime
from typing import List, Optional

from sqlalchemy import and_, func, or_
from sqlalchemy.orm import Session

from app.db.models import Event
from app.db.models import Session as SessionModel
from app.db.models import Speaker


class SessionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_sessions(self, skip: int = 0, limit: int = 100) -> List[SessionModel]:
        return self.db.query(SessionModel).offset(skip).limit(limit).all()

    def get_sessions_by_event(
        self, event_id: int, skip: int = 0, limit: int = 100
    ) -> List[SessionModel]:
        return (
            self.db.query(SessionModel)
            .filter(SessionModel.event_id == event_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_sessions_count(self) -> int:
        return self.db.query(func.count(SessionModel.id)).scalar() or 0

    def get_sessions_count_by_event(self, event_id: int) -> int:
        return (
            self.db.query(func.count(SessionModel.id))
            .filter(SessionModel.event_id == event_id)
            .scalar()
            or 0
        )

    def get_session_by_id(self, session_id: int) -> SessionModel:
        return self.db.query(SessionModel).filter(SessionModel.id == session_id).first()

    def create_session(self, session: SessionModel) -> SessionModel:
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session

    def update_session(self, session_id: int, session_data: dict) -> SessionModel:
        session = (
            self.db.query(SessionModel).filter(SessionModel.id == session_id).first()
        )
        if session:
            for key, value in session_data.items():
                if value is not None:
                    setattr(session, key, value)
            self.db.commit()
            self.db.refresh(session)
        return session

    def delete_session(self, session_id: int) -> bool:
        session = (
            self.db.query(SessionModel).filter(SessionModel.id == session_id).first()
        )
        if session:
            self.db.delete(session)
            self.db.commit()
            return True
        return False

    def check_schedule_conflicts(
        self,
        event_id: int,
        start_time: datetime,
        end_time: datetime,
        exclude_session_id: Optional[int] = None,
    ) -> List[SessionModel]:
        """Check for schedule conflicts with existing sessions"""
        query = self.db.query(SessionModel).filter(
            and_(
                SessionModel.event_id == event_id,
                SessionModel.is_active == True,
                or_(
                    and_(
                        SessionModel.start_time < end_time,
                        SessionModel.end_time > start_time,
                    ),
                    and_(
                        SessionModel.start_time >= start_time,
                        SessionModel.start_time < end_time,
                    ),
                    and_(
                        SessionModel.end_time > start_time,
                        SessionModel.end_time <= end_time,
                    ),
                ),
            )
        )

        if exclude_session_id:
            query = query.filter(SessionModel.id != exclude_session_id)

        return query.all()

    def get_event_by_id(self, event_id: int) -> Event:
        """Get event by ID for validation purposes"""
        return self.db.query(Event).filter(Event.id == event_id).first()

    def get_speaker_by_id(self, speaker_id: int) -> Speaker:
        """Get speaker by ID for validation purposes"""
        return self.db.query(Speaker).filter(Speaker.id == speaker_id).first()
