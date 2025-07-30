from logging.config import fileConfig
import os
import pathlib

from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlmodel import SQLModel

# ------------------------------------------------------------------
# 1) Cargar variables de entorno (.env) para obtener DATABASE_URL
# ------------------------------------------------------------------
from dotenv import load_dotenv

load_dotenv(pathlib.Path(__file__).parent.parent / ".env")

# ------------------------------------------------------------------
# 2) Obtener el objeto de configuración de Alembic
# ------------------------------------------------------------------
config = context.config

# Inyectar la URL leída del .env en la configuración de Alembic
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))

# ------------------------------------------------------------------
# 3) Configurar el logging (opcional, ya venía por defecto)
# ------------------------------------------------------------------
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ------------------------------------------------------------------
# 4) Importar los modelos para que Alembic detecte las tablas
# ------------------------------------------------------------------
import models  # noqa: F401  (registra Colonia, Gato, Evento)

target_metadata = SQLModel.metadata  # <-- todas las tablas

# ------------------------------------------------------------------
# 5) Funciones estándar de Alembic (sin cambios)
# ------------------------------------------------------------------
def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
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
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
