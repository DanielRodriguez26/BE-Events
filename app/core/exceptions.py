from typing import Optional, List, Any
from datetime import datetime
from fastapi import HTTPException, status
from app.api.schemas.error_schemas import ErrorDetail


class BaseAPIException(HTTPException):
    """Excepción base para errores de la API"""
    
    def __init__(
        self,
        status_code: int,
        message: str,
        error_type: str = "API Error",
        details: Optional[List[ErrorDetail]] = None,
        path: Optional[str] = None,
        method: Optional[str] = None
    ):
        self.error_type = error_type
        self.details = details or []
        self.path = path
        self.method = method
        self.timestamp = datetime.utcnow()
        
        # Crear respuesta de error estructurada
        error_response = {
            "success": False,
            "error": error_type,
            "message": message,
            "details": [detail.dict() for detail in self.details] if self.details else None,
            "timestamp": self.timestamp.isoformat(),
            "path": self.path,
            "method": self.method,
            "status_code": status_code
        }
        
        super().__init__(status_code=status_code, detail=error_response)


class ValidationException(BaseAPIException):
    """Excepción para errores de validación"""
    
    def __init__(
        self,
        message: str = "Validation error",
        details: Optional[List[ErrorDetail]] = None,
        path: Optional[str] = None,
        method: Optional[str] = None
    ):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            message=message,
            error_type="Validation Error",
            details=details,
            path=path,
            method=method
        )


class AuthenticationException(BaseAPIException):
    """Excepción para errores de autenticación"""
    
    def __init__(
        self,
        message: str = "Authentication failed",
        path: Optional[str] = None,
        method: Optional[str] = None
    ):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message=message,
            error_type="Authentication Error",
            path=path,
            method=method
        )


class AuthorizationException(BaseAPIException):
    """Excepción para errores de autorización"""
    
    def __init__(
        self,
        message: str = "Insufficient permissions",
        path: Optional[str] = None,
        method: Optional[str] = None
    ):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            message=message,
            error_type="Authorization Error",
            path=path,
            method=method
        )


class NotFoundException(BaseAPIException):
    """Excepción para recursos no encontrados"""
    
    def __init__(
        self,
        message: str = "Resource not found",
        path: Optional[str] = None,
        method: Optional[str] = None
    ):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            message=message,
            error_type="Not Found",
            path=path,
            method=method
        )


class ConflictException(BaseAPIException):
    """Excepción para conflictos (409)"""
    
    def __init__(
        self,
        message: str = "Resource conflict",
        path: Optional[str] = None,
        method: Optional[str] = None
    ):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            message=message,
            error_type="Conflict",
            path=path,
            method=method
        )


class ServerException(BaseAPIException):
    """Excepción para errores internos del servidor"""
    
    def __init__(
        self,
        message: str = "Internal server error",
        path: Optional[str] = None,
        method: Optional[str] = None
    ):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=message,
            error_type="Internal Server Error",
            path=path,
            method=method
        )


def create_validation_error(field: str, message: str, value: Any = None) -> ErrorDetail:
    """Función helper para crear errores de validación"""
    return ErrorDetail(field=field, message=message, value=value)
