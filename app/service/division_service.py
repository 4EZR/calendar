# app/services/division_service.py
from app.repository.division_repository import DivisionRepository
from app.schemas.division_schema import Division as DivisionSchema, DivisionCreate, DivisionUpdate
from app.schemas.response_schema import ResponseModel
from typing import List

class DivisionService:
    def __init__(self):
        self.repository = DivisionRepository()

    def get_all_divisions(self, include_deleted: bool = False) -> ResponseModel[List[DivisionSchema]]:
        divisions = self.repository.get_all(include_deleted)
        return ResponseModel(
            success=True,
            message="Divisions retrieved successfully",
            data=[DivisionSchema.model_validate(d.to_dict()) for d in divisions]
        )

    def get_division(self, division_id: int, include_deleted: bool = False) -> ResponseModel[DivisionSchema]:
        division = self.repository.get_by_id(division_id, include_deleted)
        return ResponseModel(
            success=True,
            message="Division retrieved successfully",
            data=DivisionSchema.model_validate(division.to_dict())
        )

    def create_division(self, division_data: DivisionCreate) -> ResponseModel[DivisionSchema]:
        new_division = self.repository.create(division_data.model_dump())
        return ResponseModel(
            success=True,
            message="Division created successfully",
            data=DivisionSchema.model_validate(new_division.to_dict())
        )

    def update_division(self, division_id: int, division_data: DivisionUpdate) -> ResponseModel[DivisionSchema]:
        updated_division = self.repository.update(division_id, division_data.model_dump(exclude_unset=True))
        return ResponseModel(
            success=True,
            message="Division updated successfully",
            data=DivisionSchema.model_validate(updated_division.to_dict())
        )

    def delete_division(self, division_id: int) -> ResponseModel[DivisionSchema]:
        deleted_division = self.repository.soft_delete(division_id)
        return ResponseModel(
            success=True,
            message="Division deleted successfully",
            data=DivisionSchema.model_validate(deleted_division.to_dict())
        )

    def restore_division(self, division_id: int) -> ResponseModel[DivisionSchema]:
        restored_division = self.repository.restore(division_id)
        return ResponseModel(
            success=True,
            message="Division restored successfully",
            data=DivisionSchema.model_validate(restored_division.to_dict())
        )