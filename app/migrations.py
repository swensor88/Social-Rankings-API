from alembic import command
from alembic.config import Config

from app.config import settings


def run_startup_migrations() -> None:
    """Apply latest Alembic migrations at application startup."""
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", settings.database_url)
    command.upgrade(alembic_cfg, "head")
