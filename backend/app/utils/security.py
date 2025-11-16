from datetime import datetime, timedelta
from typing import Any, Dict

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from app.core.config import get_settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def create_access_token(subject: str, expires_delta: timedelta | None = None) -> str:
    settings = get_settings()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
    to_encode: Dict[str, Any] = {"sub": subject, "exp": expire}
    return jwt.encode(to_encode, settings.secret_key, algorithm="HS256")


def verify_credentials(username: str, password: str) -> bool:
    settings = get_settings()
    return username == settings.admin_username and password == settings.admin_password


def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    settings = get_settings()
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
    except JWTError as exc:
        raise credentials_exception from exc

    username: str | None = payload.get("sub")
    if username is None:
        raise credentials_exception
    if username != settings.admin_username:
        raise credentials_exception
    return username
