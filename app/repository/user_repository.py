from pony.orm import db_session, select
from app.models import user
from datetime import datetime
from app.config.database import get_db

class UseerRepository:
    def __init__(self):
        self.db = get_db()

    @db_session
    def get_all(self, include_deleted=False):
        if include_deleted:
            return list(select(d for d in user))
        return list(select(d for d in user if d.deleted_at is None))

    @db_session
    def get_by_id(self, user_id: int, include_deleted=False):
        if include_deleted:
            return user.get(id=user_id)
        return user.get(lambda d: d.id == user_id and d.deleted_at is None)

    @db_session
    def create(self, user_data):
        return user(**user_data)

    @db_session
    def update(self, user_id: int, user_data):
        user = user.get(lambda d: d.id == user_id and d.deleted_at is None)
        if user:
            user.set(**user_data)
        return user

    @db_session
    def soft_delete(self, user_id: int):
        user = user.get(lambda d: d.id == user_id and d.deleted_at is None)
        if user:
            user.soft_delete()
        return user

    @db_session
    def restore(self, user_id: int):
        user = user.get(lambda d: d.id == user_id and d.deleted_at is not None)
        if user:
            user.deleted_at = None
        return user