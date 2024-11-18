from typing import Generic, TypeVar, Optional, List
from pydantic import BaseModel

T = TypeVar('T')

class ResponseModel(BaseModel, Generic[T]):
    success: bool
    message: str
    data: Optional[T] = None

class ErrorDetail(BaseModel):
    field: Optional[str] = None
    message: str

class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    errors: List[ErrorDetail]

class PaginatedResponse(ResponseModel[List[T]], Generic[T]):
    total: int
    page: int
    size: int
    pages: int