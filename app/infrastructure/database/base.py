import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

# URL de conexión a la base de datos
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:1234@localhost:5432/myevents",
)

# Crear engine y fábrica de sesiones
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)


def init_db() -> None:
    """Crea las tablas si no existen. Usar solo en dev/testing.
    En producción, usa Alembic para migraciones.
    """
    SQLModel.metadata.create_all(bind=engine)
