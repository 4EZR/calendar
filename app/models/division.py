from pony.orm import Required,PrimaryKey, Optional, Set
from datetime import datetime
from app.config.database import db

class Division(db.Entity):
    _table_ = 'divisions'
    id = PrimaryKey(int, auto=True)
    name = Required(str, 255)
    created_at = Optional(datetime)
    updated_at = Optional(datetime)
    deleted_at = Optional(datetime)
    color = Optional(str, 255)
    code = Optional(str, 255)
    type = Optional(str, 255)
    # users = Set('User')
