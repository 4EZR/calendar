from pony.orm import db_session, select
from app.models.division import Division
from datetime import datetime
from app.config.database import get_db

class DivisionRepository:
    def __init__(self):
        self.db = get_db()

    @db_session
    def get_all(self, include_deleted=False):
        if include_deleted:
            return list(select(d for d in Division))
        return list(select(d for d in Division if d.deleted_at is None))

    @db_session
    def get_by_id(self, division_id: int, include_deleted=False):
        if include_deleted:
            return Division.get(id=division_id)
        return Division.get(lambda d: d.id == division_id and d.deleted_at is None)

    @db_session
    def create(self, division_data):
        division_data['created_at'] = datetime.now()
        return Division(**division_data)

    @db_session
    def update(self, division_id: int, division_data):
        division = Division.get(lambda d: d.id == division_id and d.deleted_at is None)
        if division:
            division_data['updated_at'] = datetime.now()
            division.set(**division_data)
        return division

    @db_session
    def soft_delete(self, division_id: int):
        division = Division.get(lambda d: d.id == division_id and d.deleted_at is None)
        if division:
            division.deleted_at = datetime.now()
        return division

    @db_session
    def restore(self, division_id: int):
        division = Division.get(lambda d: d.id == division_id and d.deleted_at is not None)
        if division:
            division.deleted_at = None
        return division