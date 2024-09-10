from pony.orm import Database, set_sql_debug
from dotenv import load_dotenv
import os


load_dotenv()

db = Database()

def get_db():
    return db

def init_db():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    db.bind(provider='mysql', host='localhost', user='root', passwd='', db='psb_kalender_fastapi')
    db.generate_mapping(create_tables=True)
    set_sql_debug(True) 