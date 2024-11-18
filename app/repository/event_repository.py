# app/repository/event_repository.py
from pony.orm import db_session, select
from app.models import Event, EventDateRange, EventVisibility, User, Division, Department
from datetime import datetime, timedelta
from app.config.database import get_db
from app.config.exception import NotFoundError, BadRequestError

class EventRepository:
    def __init__(self):
        self.db = get_db()

    @db_session
    def get_events_for_user(self, user_email, highlighted_only=False, upcoming_month=False, today_only=False):
        try:
            user = User.get(email=user_email)
            if not user:
                raise NotFoundError(f"User with email {user_email} not found")

            events = select(e for e in Event if 
                e.scope == 'global' or
                (e.scope == 'division' and e.host_division == user.division) or
                (e.scope == 'department' and e.host_department == user.department) or
                (e.scope == 'custom' and 
                (EventVisibility.exists(lambda ev: ev.event == e and 
                (ev.division == user.division or ev.department == user.department)))
                )
            )

            if highlighted_only:
                events = events.filter(lambda e: e.highlight == True)

            if upcoming_month or today_only:
                today = datetime.now().date()
                if upcoming_month:
                    end_date = today + timedelta(days=30)
                else:  # today_only
                    end_date = today

                events = events.filter(lambda e: EventDateRange.exists(
                    lambda edr: edr.event == e and 
                    ((edr.start_date <= end_date) and (edr.end_date >= today))
                ))

            return list(events)
        except Exception as e:
            raise BadRequestError(f"Error retrieving events: {str(e)}")

    @db_session
    def get_event_details(self, event_id):
        try:
            event = Event.get(id=event_id)
            if not event:
                raise NotFoundError(f"Event with id {event_id} not found")

            date_ranges = list(EventDateRange.select(lambda edr: edr.event == event))
            visibility = list(EventVisibility.select(lambda ev: ev.event == event))

            return {
                "id": str(event.id),
                "title": event.title,
                "description": event.description,
                "color": event.host_division.color if event.host_division else "#000000",
                "highlight": event.highlight,
                "open_to_all": event.scope == 'global',
                "host": event.host_division.name if event.host_division else (event.host_department.name if event.host_department else "Unknown"),
                "dateRanges": [{"start": dr.start_date.strftime("%Y-%m-%d"), "end": dr.end_date.strftime("%Y-%m-%d")} for dr in date_ranges],
                "division_access": [str(v.division.id) for v in visibility if v.division]
            }
        except NotFoundError:
            raise
        except Exception as e:
            raise BadRequestError(f"Error retrieving event details: {str(e)}")

    @db_session
    def create_event(self, event_data):
        try:
            return Event(**event_data)
        except ValueError as e:
            raise BadRequestError(f"Invalid event data: {str(e)}")
        except Exception as e:
            raise BadRequestError(f"Error creating event: {str(e)}")

    @db_session
    def update_event(self, event_id, event_data):
        try:
            event = Event.get(id=event_id)
            if not event:
                raise NotFoundError(f"Event with id {event_id} not found")
            event.set(**event_data)
            return event
        except NotFoundError:
            raise
        except ValueError as e:
            raise BadRequestError(f"Invalid update data: {str(e)}")
        except Exception as e:
            raise BadRequestError(f"Error updating event: {str(e)}")

    @db_session
    def delete_event(self, event_id):
        try:
            event = Event.get(id=event_id)
            if not event:
                raise NotFoundError(f"Event with id {event_id} not found")
            event.delete()
            return True
        except NotFoundError:
            raise
        except Exception as e:
            raise BadRequestError(f"Error deleting event: {str(e)}")