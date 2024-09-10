from app.repository.division_repository import DivisionRepository
from app.schemas.division_schema import DivisionCreate, DivisionUpdate

class DivisionService:
    def __init__(self):
        self.repository = DivisionRepository()

    def get_all_divisions(self, include_deleted=False):
        return self.repository.get_all(include_deleted)

    def get_division(self, division_id: int, include_deleted=False):
        return self.repository.get_by_id(division_id, include_deleted)

    def create_division(self, division: DivisionCreate):
        division_data = division.dict()
        return self.repository.create(division_data)

    def update_division(self, division_id: int, division: DivisionUpdate):
        division_data = division.dict(exclude_unset=True)
        return self.repository.update(division_id, division_data)

    def delete_division(self, division_id: int):
        return self.repository.soft_delete(division_id)

    def restore_division(self, division_id: int):
        return self.repository.restore(division_id)