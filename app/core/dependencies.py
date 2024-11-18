from fastapi import Depends
from .security import APIKeyValidator


require_calendar_key = Depends(APIKeyValidator.validate_calendar_key)
require_sas_key = Depends(APIKeyValidator.validate_sas_key)