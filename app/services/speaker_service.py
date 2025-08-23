import math
from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from app.api.schemas.speaker_schemas import Speaker
from app.infrastructure.repositories.speaker_repository import SpeakerRepository


class SpeakerService:
    def __init__(self, db: Session):
        self.db = db
        self.speaker_repository = SpeakerRepository(db)

    def get_all_speakers(self) -> List[Speaker]:
        speakers = self.speaker_repository.get_all_speakers()
        return [Speaker.from_orm(speaker) for speaker in speakers]
