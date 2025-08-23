from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.schemas.speaker_schemas import Speaker
from app.db.base import get_db
from app.services.speaker_service import SpeakerService

router = APIRouter()


@router.get("/", response_model=List[Speaker], summary="Get all speakers")
async def get_all_speakers(db: Session = Depends(get_db)):
    """
    Retrieve all speakers.
    """
    try:
        speaker_service = SpeakerService(db)
        speakers = speaker_service.get_all_speakers()

        return speakers
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
