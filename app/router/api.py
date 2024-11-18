from fastapi import APIRouter
from app.router.v1 import division, event, department
from app.router.v1.sas import event as sas_event
from app.core.dependencies import require_calendar_key, require_sas_key

router = APIRouter()

router.include_router(division.router, prefix="/v1/divisions", tags=["divisions"], dependencies=[require_calendar_key])
router.include_router(event.router, prefix="/v1/events", tags=["events"],dependencies=[require_calendar_key])
router.include_router(department.router, prefix = '/v1/department', tags=["departments"],dependencies=[require_calendar_key])
router.include_router(sas_event.router, prefix="/v1/sas/events", tags=["sas-events"],dependencies=[require_sas_key])
