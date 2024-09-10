# alembic/env.py
from app.config.settings import settings

config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)