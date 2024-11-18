from fastapi import Security
from fastapi.security import APIKeyHeader
import os
from typing import Optional
from app.config.exception import UnauthorizedError, ForbiddenError
import logging

logger = logging.getLogger(__name__)

# Initialize API key header
API_KEY_HEADER = APIKeyHeader(name="X-API-KEY", auto_error=False)

class APIKeyValidator:
    @staticmethod
    async def validate_api_key(api_key: Optional[str] = Security(API_KEY_HEADER)) -> str:
        """Base API key validation"""
        if not api_key:
            raise UnauthorizedError(detail="API Key header is missing")
        return api_key

    @staticmethod
    async def validate_calendar_key(api_key: Optional[str] = Security(API_KEY_HEADER)) -> str:
        """Calendar API specific validation"""
        if not api_key:
            raise UnauthorizedError(detail="API Key header is missing")
        
        calendar_api_key = os.getenv('CALENDAR_API_KEY')
        if api_key != calendar_api_key:
            raise ForbiddenError(detail="Invalid Calendar API key")
            
        logger.info("Successful Calendar API key validation")
        return api_key

    @staticmethod
    async def validate_sas_key(api_key: Optional[str] = Security(API_KEY_HEADER)) -> str:
        """SAS API specific validation"""
        if not api_key:
            raise UnauthorizedError(detail="API Key header is missing")
        
        sas_api_key = os.getenv('SAS_API_KEY')
        if api_key != sas_api_key:
            raise ForbiddenError(detail="Invalid SAS API key")
            
        logger.info("Successful SAS API key validation")
        return api_key