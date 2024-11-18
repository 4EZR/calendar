from pydantic import BaseModel
from typing import Optional
from datetime import datetime
class DepartmentBase(BaseModel):
    name: str
    color: Optional[str] = None
    code: Optional[str] = None
    type: Optional[str] = None
class DepartmentCreate(DepartmentBase):
    pass
class DepartmentUpdate(DepartmentBase):
    pass
class Department(DepartmentBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_deleted: bool
    deleted_at: Optional[datetime] = None
    class Config:
        orm_mode = True