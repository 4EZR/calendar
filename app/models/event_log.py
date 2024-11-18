# models/event_log.py
from pony.orm import PrimaryKey, Required, Optional
from datetime import datetime
from enum import Enum
from app.config.database import db

class ActionType(Enum):
    CREATE = 'create'
    UPDATE = 'update'
    DELETE = 'delete'

class EventLog(db.Entity):
    _table_ = 'event_logs'
    
    id = PrimaryKey(int, auto=True, unsigned=True)
    event = Required('Event')
    user = Required('User')
    action = Required(str)
    details = Optional(str)
    created_at = Required(datetime, default=lambda: datetime.now())