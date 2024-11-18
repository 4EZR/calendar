from pony.orm import PrimaryKey, Required, Optional, Set
from enum import Enum
from app.config.database import db
from datetime import datetime, timezone

class ScopeType(Enum):
    ALL = 'all'
    DIVISION = 'division'
    DEPARTMENT = 'department'
    CUSTOM = 'custom'

class HostType(Enum):
    DIVISION = 'division'
    DEPARTMENT = 'department'
    NONE = 'none'


class Event(db.Entity):
    _table_ = 'events'
    
    id = PrimaryKey(int, auto=True, unsigned=True)
    title = Required(str)
    description = Required(str)
    highlight = Required(bool)
    scope = Required(str)
    host_type = Required(str)
    
    created_by = Required('User', reverse='created_events')
    updated_by = Optional('User', reverse='updated_events')
    host_division = Optional('Division', reverse='hosted_events')
    host_department = Optional('Department', reverse='hosted_events')
    
    date_ranges = Set('EventDateRange')
    logs = Set('EventLog')
    visibility = Set('EventVisibility')
    
    # Timestamp attributes
    created_at = Required(datetime, default=lambda: datetime.now(timezone.utc))
    updated_at = Required(datetime, default=lambda: datetime.now(timezone.utc))


    def before_update(self):
        self.updated_at = datetime.now(timezone.utc)
