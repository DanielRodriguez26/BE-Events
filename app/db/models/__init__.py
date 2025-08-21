# Import all models here to ensure they are registered with SQLAlchemy
from app.db.models.event_models import Event
from app.db.models.event_register_models import EventRegistration
from app.db.models.rol_models import Role
from app.db.models.session_models import Session
from app.db.models.speaker_model import Speaker
from app.db.models.user_model import User

# This ensures all models are imported and their metadata is available
__all__ = ["Event", "EventRegistration", "Role", "User", "Session", "Speaker"]
