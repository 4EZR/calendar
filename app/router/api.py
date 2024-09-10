from fastapi import APIRouter
from app.router.v1 import division

router = APIRouter()

router.include_router(division.router, prefix="/v1/divisions", tags=["divisions"])