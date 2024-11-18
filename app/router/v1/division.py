from fastapi import APIRouter, Depends
from typing import List
from app.schemas.division_schema import Division, DivisionCreate, DivisionUpdate
from app.schemas.response_schema import ResponseModel
from app.service.division_service import DivisionService

router = APIRouter()

def get_division_service():
    return DivisionService()

@router.get("/", response_model=ResponseModel[List[Division]])
def get_all_divisions(include_deleted: bool = False, service: DivisionService = Depends(get_division_service)):
    return service.get_all_divisions(include_deleted)

@router.get("/{division_id}", response_model=ResponseModel[Division])
def get_division(division_id: int, include_deleted: bool = False, service: DivisionService = Depends(get_division_service)):
    return service.get_division(division_id, include_deleted)

@router.post("/", response_model=ResponseModel[Division], status_code=201)
def create_division(division: DivisionCreate, service: DivisionService = Depends(get_division_service)):
    return service.create_division(division)

@router.put("/{division_id}", response_model=ResponseModel[Division])
def update_division(division_id: int, division: DivisionUpdate, service: DivisionService = Depends(get_division_service)):
    return service.update_division(division_id, division)

@router.delete("/{division_id}", response_model=ResponseModel[Division])
def delete_division(division_id: int, service: DivisionService = Depends(get_division_service)):
    return service.delete_division(division_id)

@router.post("/{division_id}/restore", response_model=ResponseModel[Division])
def restore_division(division_id: int, service: DivisionService = Depends(get_division_service)):
    return service.restore_division(division_id)