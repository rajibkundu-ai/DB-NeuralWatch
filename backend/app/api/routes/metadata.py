from fastapi import APIRouter, Depends

from app.core.config import get_settings
from app.utils.connection import extract_connection_details
from app.utils.security import get_current_user

router = APIRouter(prefix="/metadata", tags=["metadata"], dependencies=[Depends(get_current_user)])

settings = get_settings()


@router.get("/connection")
def connection_info():
    host, database = extract_connection_details(settings.sqlserver_connection_string)
    return {
        "app": settings.app_name,
        "host": host,
        "database": database,
    }
