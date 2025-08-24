from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel, ConfigDict


class ErrorDetail(BaseModel):
    """Detalle específico de un error de validación"""

    field: Optional[str] = None
    message: str
    value: Optional[Any] = None


class ErrorResponse(BaseModel):
    """Respuesta de error estandarizada"""

    model_config = ConfigDict(json_encoders={datetime: lambda v: v.isoformat()})

    success: bool = False
    error: str
    message: str
    details: Optional[List[ErrorDetail]] = None
    timestamp: datetime
    path: Optional[str] = None
    method: Optional[str] = None
    status_code: int


class ValidationErrorResponse(ErrorResponse):
    """Respuesta específica para errores de validación"""

    error: str = "Validation Error"
    details: List[ErrorDetail]


class AuthenticationErrorResponse(ErrorResponse):
    """Respuesta específica para errores de autenticación"""

    error: str = "Authentication Error"


class AuthorizationErrorResponse(ErrorResponse):
    """Respuesta específica para errores de autorización"""

    error: str = "Authorization Error"


class NotFoundErrorResponse(ErrorResponse):
    """Respuesta específica para recursos no encontrados"""

    error: str = "Not Found"


class ServerErrorResponse(ErrorResponse):
    """Respuesta específica para errores del servidor"""

    error: str = "Internal Server Error"
