# models/event_date_range.py
from pony.orm import PrimaryKey, Required
from datetime import datetime
from app.config.database import db



class EventDateRange(db.Entity):
    _table_ = 'event_date_ranges'
    
    id = PrimaryKey(int, auto=True, unsigned=True)
    event = Required('Event')
    start_date = Required(datetime)
    end_date = Required(datetime)
    
    
