from fastapi import APIRouter, Depends
from typing import List
from app.schemas import Department, DepartmentCreate, DepartmentUpdate
from app.schemas.response_schema import ResponseModel
from app.service import DepartmentService

router = APIRouter()

def get_department_service():
    return DepartmentService()

@router.get("/", response_model=ResponseModel[List[Department]])
def get_all_departments(include_deleted: bool = False, service: DepartmentService = Depends(get_department_service)):
    return service.get_all_departments(include_deleted)

@router.get("/{department_id}", response_model=ResponseModel[Department])
def get_department(department_id: int, include_deleted: bool = False, service: DepartmentService = Depends(get_department_service)):
    return service.get_department_by_id(department_id, include_deleted)

@router.post("/", response_model=ResponseModel[Department], status_code=201)
def create_department(department: DepartmentCreate, service: DepartmentService = Depends(get_department_service)):
    return service.create_department(department)

@router.put("/{department_id}", response_model=ResponseModel[Department])
def update_department(department_id: int, department: DepartmentUpdate, service: DepartmentService = Depends(get_department_service)):
    return service.update_department(department_id, department)

@router.delete("/{department_id}", response_model=ResponseModel[Department])
def delete_department(department_id: int, service: DepartmentService = Depends(get_department_service)):
    return service.delete_department(department_id)

@router.post("/{department_id}/restore", response_model=ResponseModel[Department])
def restore_department(department_id: int, service: DepartmentService = Depends(get_department_service)):
    return service.restore_department(department_id)