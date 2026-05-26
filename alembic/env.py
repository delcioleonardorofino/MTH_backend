from logging.config import fileConfig

from sqlalchemy import create_engine
from sqlalchemy import pool

from alembic import context

from app.core.config import DATABASE_URL
from app.models.base import Base

config = context.config

config.set_main_option("sqlalchemy.url", DATABASE_URL)

target_metadata = Base.metadata

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def get_sync_url():
    url = config.get_main_option("sqlalchemy.url")

    if url.startswith("postgresql+asyncpg"):
        url = url.replace("postgresql+asyncpg", "postgresql", 1)

    return url


def run_migrations_offline() -> None:
    url = get_sync_url()

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    url = get_sync_url()

    connectable = create_engine(
        url,
        poolclass=pool.NullPool
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()