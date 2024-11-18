from fastapi import APIRouter, Depends, HTTPException
from app.service.event_service import EventService
from app.schemas.event_schema import EventCreateSchema, EventUpdateSchema
from app.schemas.response_schema import ResponseModel
from typing import List

router = APIRouter()

def get_event_service():
    return EventService()

@router.get("/", response_model=ResponseModel[List[dict]])
async def get_events(user_email: str, service: EventService = Depends(get_event_service)):
    return service.get_events_for_user(user_email)

@router.get("/highlighted", response_model=ResponseModel[List[dict]])
async def get_highlighted_events(user_email: str, service: EventService = Depends(get_event_service)):
    return service.get_highlighted_events_for_user(user_email)

@router.get("/upcoming-month", response_model=ResponseModel[List[dict]])
async def get_upcoming_month_events(user_email: str, service: EventService = Depends(get_event_service)):
    return service.get_upcoming_month_events_for_user(user_email)

@router.get("/today", response_model=ResponseModel[List[dict]])
async def get_today_events(user_email: str, service: EventService = Depends(get_event_service)):
    return service.get_today_events_for_user(user_email)

@router.post("/", response_model=ResponseModel[dict])
async def create_event(event_data: EventCreateSchema, service: EventService = Depends(get_event_service)):
    return service.create_event(event_data.dict())

@router.put("/{event_id}", response_model=ResponseModel[dict])
async def update_event(event_id: int, event_data: EventUpdateSchema, service: EventService = Depends(get_event_service)):
    return service.update_event(event_id, event_data.dict(exclude_unset=True))

@router.delete("/{event_id}", response_model=ResponseModel[bool])
async def delete_event(event_id: int, service: EventService = Depends(get_event_service)):
    return service.delete_event(event_id)