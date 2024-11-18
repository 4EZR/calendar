# config/database.py
from pony.orm import Database, sql_debug
from dotenv import load_dotenv
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

db = Database()

def get_db():
    return db

def init_db():
    try:
        sql_debug(True)
        logger.info("Initializing database connection...")
        db.bind(
            provider='postgres',
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            port=int(os.getenv('DB_PORT'))
        )

        logger.info("Database connection established.")

        logger.info("Generating mapping...")
        if not db.schema:
            db.generate_mapping(create_tables=True)
        logger.info("Mapping generated successfully.")
        logger.info("Mapped entities:")
        for entity_name, entity in db.entities.items():
            logger.info(f"Entity: {entity_name}")
            logger.info(f"  Attributes: {', '.join(attr.name for attr in entity._attrs_)}")
            logger.info(f"  Table: {entity._table_}")
            logger.info("---")

    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise

    logger.info("Database initialization completed.")
