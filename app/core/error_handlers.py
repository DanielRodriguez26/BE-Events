from datetime import datetime
from typing import Union

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.api.schemas.error_schemas import ErrorDetail, ErrorResponse
from app.core.exceptions import BaseAPIException


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Manejador para errores de validación de Pydantic"""
    details = []

    for error in exc.errors():
        detail = ErrorDetail(
            field=error.get("loc", [None])[-1] if error.get("loc") else None,
            message=error.get("msg", "Validation error"),
            value=error.get("input"),
        )
        details.append(detail)

    error_response = ErrorResponse(
        success=False,
        error="Validation Error",
        message="Los datos proporcionados no son válidos",
        details=details,
        timestamp=datetime.utcnow(),
        path=str(request.url.path),
        method=request.method,
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=error_response.model_dump(mode="json"),
    )


async def custom_exception_handler(request: Request, exc: BaseAPIException):
    """Manejador para excepciones personalizadas de la API"""
    return JSONResponse(status_code=exc.status_code, content=exc.detail)


async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """Manejador para errores de SQLAlchemy"""
    error_message = "Error en la base de datos"

    if isinstance(exc, IntegrityError):
        error_message = "Conflicto de datos en la base de datos"
        status_code = status.HTTP_409_CONFLICT
    else:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    error_response = ErrorResponse(
        success=False,
        error="Database Error",
        message=error_message,
        timestamp=datetime.utcnow(),
        path=str(request.url.path),
        method=request.method,
        status_code=status_code,
    )

    return JSONResponse(
        status_code=status_code, content=error_response.model_dump(mode="json")
    )


async def general_exception_handler(request: Request, exc: Exception):
    """Manejador general para cualquier excepción no manejada"""
    error_response = ErrorResponse(
        success=False,
        error="Internal Server Error",
        message="Ha ocurrido un error interno en el servidor",
        timestamp=datetime.utcnow(),
        path=str(request.url.path),
        method=request.method,
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response.model_dump(mode="json"),
    )


async def http_exception_handler(
    request: Request, exc: Union[Exception, BaseAPIException]
):
    """Manejador para excepciones HTTP estándar"""
    if hasattr(exc, "status_code") and hasattr(exc, "detail"):
        # Si ya es una excepción estructurada, la devolvemos tal como está
        if isinstance(exc.detail, dict) and "success" in exc.detail:
            return JSONResponse(status_code=exc.status_code, content=exc.detail)

        # Si no, la estructuramos
        error_response = ErrorResponse(
            success=False,
            error="HTTP Error",
            message=str(exc.detail),
            timestamp=datetime.utcnow(),
            path=str(request.url.path),
            method=request.method,
            status_code=exc.status_code,
        )

        return JSONResponse(
            status_code=exc.status_code, content=error_response.model_dump(mode="json")
        )

    # Fallback para excepciones no estructuradas
    return await general_exception_handler(request, exc)
