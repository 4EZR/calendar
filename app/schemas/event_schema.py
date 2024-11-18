from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

class DateRange(BaseModel):
    start: date
    end: date

class EventBaseSchema(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str
    highlight: bool = False
    scope: str = Field(..., pattern='^(global|division|department|custom)$')
    host_division: Optional[int] = None
    host_department: Optional[int] = None
    dateRanges: List[DateRange]
    division_access: Optional[List[int]] = None

class EventCreateSchema(EventBaseSchema):
    pass

class EventUpdateSchema(EventBaseSchema):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    highlight: Optional[bool] = None
    scope: Optional[str] = Field(None, pattern='^(global|division|department|custom)$')
    dateRanges: Optional[List[DateRange]] = None

class EventSchema(EventBaseSchema):
    id: str
    color: str
    open_to_all: bool
    host: str

class EventsResponse(BaseModel):
    success: bool
    data: List[EventSchema]

class EventResponse(BaseModel):
    success: bool
    data: EventSchema

class MessageResponse(BaseModel):
    success: bool
    message: str