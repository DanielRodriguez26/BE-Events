from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import settings
from app.db.base import Base, engine
from app.core.exceptions import BaseAPIException
from app.core.error_handlers import (
    validation_exception_handler,
    custom_exception_handler,
    sqlalchemy_exception_handler,
    general_exception_handler,
    http_exception_handler
)

# Importar todos los modelos para asegurar que estén registrados
from app.db.models import *
from app.routes.api import api_router

# Crear aplicación FastAPI
app = FastAPI(
    title=settings.project_name,
    debug=settings.debug,
    openapi_url=f"{settings.api_v1_str}/openapi.json",
)

# Agregar middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configurar apropiadamente para producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar manejadores de errores
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(BaseAPIException, custom_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Incluir rutas de la API
app.include_router(api_router, prefix=settings.api_v1_str)


@app.get("/")
async def root():
    """Endpoint raíz."""
    return {"message": "Welcome to Events API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    """Endpoint de verificación de salud."""
    return {"status": "healthy"}
