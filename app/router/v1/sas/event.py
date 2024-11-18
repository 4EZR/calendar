from fastapi import APIRouter, Depends, HTTPException
from app.service.event_service import EventService
from app.schemas.response_schema import ResponseModel
from typing import List

router = APIRouter()

def get_event_service():
    return EventService()

@router.get("/", response_model=ResponseModel[List[dict]])
async def get_events(user_email: str, service: EventService = Depends(get_event_service)):
    return service.get_events_for_user(user_email)
