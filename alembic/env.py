# alembic/env.py

import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# --- MODIFICACIÓN 1: Apuntar al directorio raíz del proyecto ---
# Esto permite que Alembic encuentre tu carpeta 'src'
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))
# -------------------------------------------------------------

# Importa tu Base y los modelos para que Alembic los reconozca
from app.infrastructure.database.base import Base
from app.infrastructure.database.model.event_model import EventesModel # Asegúrate de importar todos tus modelos


# este es el objeto de configuración de Alembic, que proporciona
# acceso a los valores dentro del archivo .ini en uso.
config = context.config

# Interpretar el archivo de configuración para el logging de Python.
# Esta línea configura los loggers básicamente.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- MODIFICACIÓN 2: Asignar los metadatos de tu Base ---
target_metadata = Base.metadata
# --------------------------------------------------------

# otros valores de la configuración, definidos por las necesidades de env.py,
# pueden ser adquiridos:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Ejecutar migraciones en modo 'offline'.

    Esto configura el contexto con solo una URL
    y no un Engine, aunque un Engine es aceptable
    aquí también. Al omitir la creación del Engine
    ni siquiera necesitamos que un DBAPI esté disponible.

    Las llamadas a context.execute() aquí emiten la cadena dada a la
    salida del script.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Ejecutar migraciones en modo 'online'.

    En este escenario necesitamos crear un Engine
    y asociar una conexión con el contexto.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

