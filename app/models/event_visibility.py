# models/event_visibility.py
from pony.orm import PrimaryKey, Required, Optional
from app.config.database import db


class EventVisibility(db.Entity):
    _table_ = 'event_visibility'
    
    id = PrimaryKey(int, auto=True, unsigned=True)
    event = Required('Event')
    division = Optional('Division')
    department = Optional('Department')