# app/services/department_service.py
from app.repository.department_repository import DepartmentRepository
from app.schemas.department_schema import DepartmentCreate, DepartmentUpdate, Department
from app.schemas.response_schema import ResponseModel
from typing import List

class DepartmentService:
    def __init__(self):
        self.repository = DepartmentRepository()

    def get_all_departments(self, include_deleted: bool = False) -> ResponseModel[List[Department]]:
        departments = self.repository.get_all(include_deleted)
        return ResponseModel(
            success=True,
            message="Departments retrieved successfully",
            data=[Department.from_orm(d) for d in departments]
        )

    def get_department_by_id(self, department_id: int, include_deleted: bool = False) -> ResponseModel[Department]:
        department = self.repository.get_by_id(department_id, include_deleted)
        return ResponseModel(
            success=True,
            message="Department retrieved successfully",
            data=Department.from_orm(department)
        )

    def create_department(self, department_data: DepartmentCreate) -> ResponseModel[Department]:
        created = self.repository.create(department_data.dict())
        return ResponseModel(
            success=True,
            message="Department created successfully",
            data=Department.from_orm(created)
        )

    def update_department(self, department_id: int, department_data: DepartmentUpdate) -> ResponseModel[Department]:
        updated = self.repository.update(department_id, department_data.dict(exclude_unset=True))
        return ResponseModel(
            success=True,
            message="Department updated successfully",
            data=Department.from_orm(updated)
        )

    def delete_department(self, department_id: int) -> ResponseModel[Department]:
        deleted = self.repository.soft_delete(department_id)
        return ResponseModel(
            success=True,
            message="Department deleted successfully",
            data=Department.from_orm(deleted)
        )

    def restore_department(self, department_id: int) -> ResponseModel[Department]:
        restored = self.repository.restore(department_id)
        return ResponseModel(
            success=True,
            message="Department restored successfully",
            data=Department.from_orm(restored)
        )