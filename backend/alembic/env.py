from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
from app.core.config import settings

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Override sqlalchemy.url with our settings
db_url = settings.DATABASE_URL
# Convert async SQLite URL to sync for Alembic
if db_url.startswith("sqlite+aiosqlite:"):
    db_url = db_url.replace("sqlite+aiosqlite:", "sqlite:")
config.set_main_option("sqlalchemy.url", db_url)

# Override the SQLAlchemy URL for Alembic to use synchronous SQLite
# Alembic does not support async engines, so we use a synchronous URL
# We'll use the same database file but with the synchronous SQLite driver
# Convert the async URL to synchronous: replace the protocol and keep the rest.
# Example: "sqlite+aiosqlite:///./test.db" -> "sqlite:///./test.db"
if settings.DATABASE_URL.startswith("sqlite+aiosqlite://"):
    # Keep the part after "://" (which includes the three slashes and the path)
    sync_url = "sqlite://" + settings.DATABASE_URL.split("://", 1)[1]
else:
    # Fallback: replace the prefix (for other databases)
    sync_url = settings.DATABASE_URL.replace("sqlite+aiosqlite://", "sqlite:///")
config.set_section_option(config.config_ini_section, "sqlalchemy.url", sync_url)

# Print the URL for debugging
print(f"Alembic using SQLAlchemy URL: {sync_url}")

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
from app.db.base import Base
# Import all models here to ensure they are registered with SQLAlchemy
from app.models import user, profile, role, category, product, product_image, product_tag, tag, address, seller  # noqa
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

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
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

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
