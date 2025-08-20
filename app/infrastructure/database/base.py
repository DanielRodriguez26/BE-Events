from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL de conexión a la base de datos.
# Este ejemplo usa SQLite, que guarda la base de datos en un archivo local.
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1234@localhost:5432/myevents"
# Para PostgreSQL sería: "postgresql://user:password@postgresserver/db"

# Crea el motor de la base de datos de SQLAlchemy.
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Crea una clase SessionLocal. Cada instancia de esta clase será una sesión de base de datos.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Reutiliza la Base que creamos en models.py.
# Esto es crucial para que las herramientas de migración encuentren los modelos.
Base = declarative_base()