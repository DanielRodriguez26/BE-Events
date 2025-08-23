from typing import List

from sqlalchemy.orm import Session

from app.db.models.speaker_model import Speaker


class SpeakerRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_speakers(self) -> List[Speaker]:
        """Get all speakers."""
        return self.db.query(Speaker).all()
