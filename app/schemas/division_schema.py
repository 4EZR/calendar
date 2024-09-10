from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DivisionBase(BaseModel):
    name: str
    color: Optional[str] = None
    code: Optional[str] = None
    type: Optional[str] = None

class DivisionCreate(DivisionBase):
    pass

class DivisionUpdate(DivisionBase):
    pass

class Division(DivisionBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        orm_mode = True
