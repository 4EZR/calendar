import logging
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import JSONResponse
from app.core.security import API_KEY_HEADER
from fastapi.openapi.utils import get_openapi
import secrets
from app.config.database import init_db, db
from app.router.api import router as api_router
from app.models import *
from app.config.database_init import reset_database
from app.config.exception import NotFoundError, BadRequestError, UnauthorizedError, ForbiddenError
from app.schemas.response_schema import ErrorResponse, ErrorDetail

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

security = HTTPBasic()



app = FastAPI(
    title="API Calendar Corporate | SAS 2.0",
    description="Calendar Corporate",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

@app.exception_handler(NotFoundError)
async def not_found_exception_handler(request: Request, exc: NotFoundError):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            success=False,
            message="Not Found",
            errors=[ErrorDetail(message=str(exc.detail))]
        ).dict()
    )

@app.exception_handler(BadRequestError)
async def bad_request_exception_handler(request: Request, exc: BadRequestError):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            success=False,
            message="Bad Request",
            errors=[ErrorDetail(message=str(exc.detail))]
        ).dict()
    )

@app.exception_handler(UnauthorizedError)
async def unauthorized_exception_handler(request: Request, exc: UnauthorizedError):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            success=False,
            message="Unauthorized",
            errors=[ErrorDetail(message=str(exc.detail))]
        ).dict(),
        headers={"WWW-Authenticate": "Basic"},
    )

@app.exception_handler(ForbiddenError)
async def forbidden_exception_handler(request: Request, exc: ForbiddenError):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            success=False,
            message="Forbidden",
            errors=[ErrorDetail(message=str(exc.detail))]
        ).dict()
    )

@app.on_event("startup")
async def startup_event():
    init_db()
    # reset_database(db)

    # logger.info("Registered Pony ORM entities:")
    # for entity_name, entity in db.entities.items():
    #     logger.info(f"Entity: {entity_name}")
    #     logger.info(f"  Attributes: {', '.join(attr.name for attr in entity._attrs_)}")
    #     logger.info(f"  Table: {entity._table_}")
    #     logger.info("---")


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
        
    openapi_schema = get_openapi(
        title="API Calendar Corporate | SAS 2.0",
        version="1.0.0",
        description="Calendar Corporate",
        routes=app.routes,
    )
    
    # Remove the Basic Auth scheme and only keep API Key
    openapi_schema["components"]["securitySchemes"] = {
        "ApiKeyHeader": {
            "type": "apiKey",
            "in": "header",
            "name": "X-API-KEY",
            "description": "API key for authentication"
        }
    }
    
    # Only require API Key security
    openapi_schema["security"] = [{"ApiKeyHeader": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi


# Include API routes
app.include_router(api_router)