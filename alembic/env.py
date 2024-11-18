from logging.config import fileConfig
from alembic import context
from app.models import db

config = context.config
fileConfig(config.config_file_name)

target_metadata = db

def run_migrations_offline():
    context.configure(url=config.get_main_option("sqlalchemy.url"))
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    with db.get_connection() as connection:
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
