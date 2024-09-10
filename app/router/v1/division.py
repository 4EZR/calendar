from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from app.schemas.division_schema import Division, DivisionCreate, DivisionUpdate
from app.service.division_service import DivisionService

router = APIRouter()

def get_division_service():
    return DivisionService()

@router.get("/", response_model=List[Division])
async def get_all_divisions(include_deleted: bool = False, service: DivisionService = Depends(get_division_service)):
    return service.get_all_divisions(include_deleted)

@router.get("/{division_id}", response_model=Division)
async def get_division(division_id: int, include_deleted: bool = False, service: DivisionService = Depends(get_division_service)):
    division = service.get_division(division_id, include_deleted)
    if division is None:
        raise HTTPException(status_code=404, detail="Division not found")
    return division

@router.post("/", response_model=Division, status_code=status.HTTP_201_CREATED)
async def create_division(division: DivisionCreate, service: DivisionService = Depends(get_division_service)):
    return service.create_division(division)

@router.put("/{division_id}", response_model=Division)
async def update_division(division_id: int, division: DivisionUpdate, service: DivisionService = Depends(get_division_service)):
    updated_division = service.update_division(division_id, division)
    if updated_division is None:
        raise HTTPException(status_code=404, detail="Division not found")
    return updated_division

@router.delete("/{division_id}", response_model=Division)
async def delete_division(division_id: int, service: DivisionService = Depends(get_division_service)):
    deleted_division = service.delete_division(division_id)
    if deleted_division is None:
        raise HTTPException(status_code=404, detail="Division not found")
    return deleted_division

@router.post("/{division_id}/restore", response_model=Division)
async def restore_division(division_id: int, service: DivisionService = Depends(get_division_service)):
    restored_division = service.restore_division(division_id)
    if restored_division is None:
        raise HTTPException(status_code=404, detail="Division not found or already active")
    return restored_division