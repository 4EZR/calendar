# models/division.py
from pony.orm import PrimaryKey, Required, Optional, Set
from app.config.database import db
from datetime import datetime, timezone
class Division(db.Entity):
    _table_ = 'divisions'
    
    id = PrimaryKey(int, auto=True, unsigned=True)
    name = Required(str)
    color = Optional(str)
    code = Optional(str)
    type = Optional(str)
    
    # Relationships
    departments = Set('Department')
    users = Set('User')
    hosted_events = Set('Event', reverse='host_division')
    visible_events = Set('EventVisibility')

    created_at = Required(datetime, default=lambda: datetime.now())
    updated_at = Required(datetime, default=lambda: datetime.now())

    is_deleted = Required(bool, default=False)
    deleted_at = Optional(datetime)

    def before_update(self):
        self.updated_at = datetime.now()

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = datetime.now()

    def restore(self):
        self.is_deleted = False
        self.deleted_at = None