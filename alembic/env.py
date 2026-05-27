from logging.config import fileConfig
from urllib.parse import urlparse, urlunparse

from sqlalchemy import create_engine, pool
from alembic import context

from app.core.config import settings
from app.models.base import Base


# Alembic config
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)


# -----------------------------
# 🔥 CLEAN DATABASE URL (IMPORTANT)
# -----------------------------
def get_sync_url() -> str:
    """
    Converts async DB URL to sync-safe URL for Alembic.
    Also removes cloud-specific params that break psycopg2.
    """

    url = config.get_main_option("sqlalchemy.url")

    # 1. Convert asyncpg → sync
    if url.startswith("postgresql+asyncpg"):
        url = url.replace("postgresql+asyncpg", "postgresql", 1)

    # 2. Parse URL to clean query params
    parsed = urlparse(url)

    if parsed.query:
        params = parsed.query.split("&")

        allowed_params = []

        for p in params:
            # keep only safe params
            if p.startswith("sslmode="):
                allowed_params.append(p)

            # ❌ explicitly ignore problematic ones:
            # channel_binding, ssl, etc.

        clean_query = "&".join(allowed_params)

        parsed = parsed._replace(query=clean_query)

        url = urlunparse(parsed)

    return url


# -----------------------------
# OFFLINE MODE
# -----------------------------
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


# -----------------------------
# ONLINE MODE
# -----------------------------
def run_migrations_online() -> None:
    url = get_sync_url()

    connectable = create_engine(
        url,
        poolclass=pool.NullPool,
        connect_args={
            "sslmode": "require"  # safe place for SSL config
        }
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


# -----------------------------
# ENTRYPOINT
# -----------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()