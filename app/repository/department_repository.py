# app/repository/department_repository.py
from pony.orm import db_session, select
from app.models import Department
from datetime import datetime
from app.config.database import get_db
from app.config.exception import NotFoundError, BadRequestError

class DepartmentRepository:
    def __init__(self):
        self.db = get_db()

    @db_session
    def get_all(self, include_deleted=False):
        try:
            query = select(d for d in Department)
            if not include_deleted:
                query = query.filter(lambda d: d.deleted_at is None)
            return list(query)
        except Exception as e:
            raise BadRequestError(f"Error retrieving departments: {str(e)}")

    @db_session
    def get_by_id(self, department_id: int, include_deleted=False):
        try:
            department = Department.get(id=department_id)
            if not department or (not include_deleted and department.deleted_at is not None):
                raise NotFoundError(f"Department with id {department_id} not found")
            return department
        except NotFoundError:
            raise
        except Exception as e:
            raise BadRequestError(f"Error retrieving department: {str(e)}")

    @db_session
    def create(self, department_data):
        try:
            return Department(**department_data)
        except ValueError as e:
            raise BadRequestError(f"Invalid department data: {str(e)}")
        except Exception as e:
            raise BadRequestError(f"Error creating department: {str(e)}")

    @db_session
    def update(self, department_id: int, department_data):
        try:
            department = self.get_by_id(department_id)
            department.set(**department_data)
            return department
        except NotFoundError:
            raise
        except ValueError as e:
            raise BadRequestError(f"Invalid update data: {str(e)}")
        except Exception as e:
            raise BadRequestError(f"Error updating department: {str(e)}")

    @db_session
    def soft_delete(self, department_id: int):
        try:
            department = self.get_by_id(department_id)
            department.deleted_at = datetime.utcnow()
            department.is_deleted = True
            return department
        except NotFoundError:
            raise
        except Exception as e:
            raise BadRequestError(f"Error deleting department: {str(e)}")

    @db_session
    def restore(self, department_id: int):
        try:
            department = Department.get(lambda d: d.id == department_id and d.deleted_at is not None)
            if not department:
                raise NotFoundError(f"Deleted department with id {department_id} not found")
            department.deleted_at = None
            department.is_deleted = False
            return department
        except NotFoundError:
            raise
        except Exception as e:
            raise BadRequestError(f"Error restoring department: {str(e)}")