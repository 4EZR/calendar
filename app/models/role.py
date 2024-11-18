# models/role.py
from pony.orm import PrimaryKey, Required, Set, Optional
from app.config.database import db
from datetime import datetime, timezone


class Role(db.Entity):
    _table_ = 'roles'
    
    id = PrimaryKey(int, auto=True, unsigned=True)
    name = Required(str)
    
    users = Set('User')
    permissions = Set('Permission')
    
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