from datetime import timedelta

from fastapi import APIRouter, HTTPException, status

from app.models.schemas import LoginRequest, TokenResponse
from app.utils.security import create_access_token, verify_credentials
from app.core.config import get_settings

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest) -> TokenResponse:
    if not verify_credentials(payload.username, payload.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    token = create_access_token(payload.username, timedelta(minutes=get_settings().access_token_expire_minutes))
    return TokenResponse(access_token=token)
