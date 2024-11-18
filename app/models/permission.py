# models/permission.py
from pony.orm import PrimaryKey, Required, Optional, Set
from app.config.database import db
from datetime import datetime, timezone


class Permission(db.Entity):
    _table_ = 'permissions'
    
    id = PrimaryKey(int, auto=True, unsigned=True)
    name = Required(str)
    action = Optional(str)
    subject = Optional(str)
    
    roles = Set('Role')
    
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