from fastapi import FastAPI

from app.config.database import init_db
from app.router.api import router as api_router

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    init_db()

# Include API routes
app.include_router(api_router)

