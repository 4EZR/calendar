from pony.orm import PrimaryKey,Optional, Required, Set

from app.config.database import db
from datetime import datetime



class Department(db.Entity):
    _table_ = 'departments'
    
    id = PrimaryKey(int, auto=True, unsigned=True)
    name = Required(str)
    code = Required(str)
    division = Required('Division')
    color = Optional(str)
    # Relationships
    users = Set('User')
    hosted_events = Set('Event', reverse='host_department')
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