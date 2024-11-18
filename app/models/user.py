# models/user.py
from pony.orm import PrimaryKey, Required, Optional, Set
from app.config.database import db
from datetime import datetime, timezone


class User(db.Entity):
    _table_ = 'users'
    
    id = PrimaryKey(int, auto=True, unsigned=True)
    username = Required(str)
    email = Required(str)
    role = Required('Role')
    division = Optional('Division')
    department = Optional('Department')
    
    created_events = Set('Event', reverse='created_by')
    updated_events = Set('Event', reverse='updated_by')
    event_logs = Set('EventLog')
    
     # Timestamp attributes
    created_at = Required(datetime, default=lambda: datetime.now(timezone.utc))
    updated_at = Required(datetime, default=lambda: datetime.now(timezone.utc))

    # Soft delete attributes
    is_deleted = Required(bool, default=False)
    deleted_at = Optional(datetime)

    def before_update(self):
        self.updated_at = datetime.now(timezone.utc)

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = datetime.now(timezone.utc)

    def restore(self):
        self.is_deleted = False
        self.deleted_at = None