from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import os
from dotenv import load_dotenv
from app.database.models import Base  # Import your models

# Load environment variables
load_dotenv()

# this is the Alembic Config object
config = context.config

# Load database URL from environment variables
section = config.config_ini_section
config.set_section_option(section, "DB_USER", os.getenv("DB_USER"))
config.set_section_option(section, "DB_PASSWORD", os.getenv("DB_PASSWORD"))
config.set_section_option(section, "DB_HOST", os.getenv("DB_HOST"))
config.set_section_option(section, "DB_PORT", os.getenv("DB_PORT", "5432"))

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Add your model's MetaData object here for 'autogenerate' support
target_metadata = Base.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
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