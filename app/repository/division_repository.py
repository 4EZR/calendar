# app/repository/division_repository.py
from pony.orm import db_session, select
from app.models import Division
from datetime import datetime
from app.config.database import get_db
from app.config.exception import NotFoundError, BadRequestError

class DivisionRepository:
    def __init__(self):
        self.db = get_db()

    @db_session
    def get_all(self, include_deleted=False):
        try:
            if include_deleted:
                return list(select(d for d in Division))
            return list(select(d for d in Division if d.deleted_at is None))
        except Exception as e:
            raise BadRequestError(f"Error retrieving divisions: {str(e)}")

    @db_session
    def get_by_id(self, division_id: int, include_deleted=False):
        try:
            if include_deleted:
                division = Division.get(id=division_id)
            else:
                division = Division.get(lambda d: d.id == division_id and d.deleted_at is None)
            if not division:
                raise NotFoundError(f"Division with id {division_id} not found")
            return division
        except NotFoundError:
            raise
        except Exception as e:
            raise BadRequestError(f"Error retrieving division: {str(e)}")

    @db_session
    def create(self, division_data):
        try:
            return Division(**division_data)
        except ValueError as e:
            raise BadRequestError(f"Invalid division data: {str(e)}")
        except Exception as e:
            raise BadRequestError(f"Error creating division: {str(e)}")

    @db_session
    def update(self, division_id: int, division_data):
        try:
            division = self.get_by_id(division_id)
            division.set(**division_data)
            return division
        except NotFoundError:
            raise
        except ValueError as e:
            raise BadRequestError(f"Invalid update data: {str(e)}")
        except Exception as e:
            raise BadRequestError(f"Error updating division: {str(e)}")

    @db_session
    def soft_delete(self, division_id: int):
        try:
            division = self.get_by_id(division_id)
            division.soft_delete()
            return division
        except NotFoundError:
            raise
        except Exception as e:
            raise BadRequestError(f"Error deleting division: {str(e)}")

    @db_session
    def restore(self, division_id: int):
        try:
            division = Division.get(lambda d: d.id == division_id and d.deleted_at is not None)
            if not division:
                raise NotFoundError(f"Deleted division with id {division_id} not found")
            division.deleted_at = None
            return division
        except NotFoundError:
            raise
        except Exception as e:
            raise BadRequestError(f"Error restoring division: {str(e)}")