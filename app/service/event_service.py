from pydantic import ValidationError
from app.repository.event_repository import EventRepository
from app.schemas.event_schema import EventCreateSchema, EventUpdateSchema
from app.schemas.response_schema import ResponseModel
from typing import List

class EventService:
    def __init__(self):
        self.repository = EventRepository()

    def get_events_for_user(self, user_email) -> ResponseModel[List[dict]]:
        events = self.repository.get_events_for_user(user_email)
        event_details = [self.repository.get_event_details(event.id) for event in events]
        return ResponseModel(
            success=True,
            message="Events retrieved successfully",
            data=event_details
        )

    def get_highlighted_events_for_user(self, user_email) -> ResponseModel[List[dict]]:
        events = self.repository.get_events_for_user(user_email, highlighted_only=True)
        event_details = [self.repository.get_event_details(event.id) for event in events]
        return ResponseModel(
            success=True,
            message="Highlighted events retrieved successfully",
            data=event_details
        )

    def get_upcoming_month_events_for_user(self, user_email) -> ResponseModel[List[dict]]:
        events = self.repository.get_events_for_user(user_email, upcoming_month=True)
        event_details = [self.repository.get_event_details(event.id) for event in events]
        return ResponseModel(
            success=True,
            message="Upcoming month events retrieved successfully",
            data=event_details
        )

    def get_today_events_for_user(self, user_email) -> ResponseModel[List[dict]]:
        events = self.repository.get_events_for_user(user_email, today_only=True)
        event_details = [self.repository.get_event_details(event.id) for event in events]
        return ResponseModel(
            success=True,
            message="Today's events retrieved successfully",
            data=event_details
        )

    def create_event(self, event_data) -> ResponseModel[dict]:
        try:
            validated_data = EventCreateSchema(**event_data).dict()
            event_id = self.repository.create_event(validated_data)
            created_event = self.repository.get_event_details(event_id)
            return ResponseModel(
                success=True,
                message="Event created successfully",
                data=created_event
            )
        except ValidationError as e:
            return ResponseModel(
                success=False,
                message="Invalid event data",
                data={"errors": e.errors()}
            )

    def update_event(self, event_id, event_data) -> ResponseModel[dict]:
        try:
            validated_data = EventUpdateSchema(**event_data).dict(exclude_unset=True)
            updated_event = self.repository.update_event(event_id, validated_data)
            if updated_event:
                event_details = self.repository.get_event_details(updated_event.id)
                return ResponseModel(
                    success=True,
                    message="Event updated successfully",
                    data=event_details
                )
            return ResponseModel(
                success=False,
                message="Event not found",
                data=None
            )
        except ValidationError as e:
            return ResponseModel(
                success=False,
                message="Invalid event data",
                data={"errors": e.errors()}
            )

    def delete_event(self, event_id) -> ResponseModel[bool]:
        result = self.repository.delete_event(event_id)
        return ResponseModel(
            success=result,
            message="Event deleted successfully" if result else "Event not found",
            data=result
        )