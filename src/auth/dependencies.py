from datetime import UTC, datetime, timedelta

import jwt
from fastapi import Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from src.config.settings import settings
from src.storage.database import SessionLocal
from src.storage.models import User

COOKIE_NAME = "token"


def create_token(user_id: int, username: str) -> str:
    expire = datetime.now(UTC) + timedelta(hours=settings.jwt_expire_hours)
    payload = {
        "sub": str(user_id),
        "username": username,
        "exp": expire,
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm="HS256")


def decode_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, settings.jwt_secret_key, algorithms=["HS256"])
    except jwt.InvalidTokenError:
        return None


def get_current_user(request: Request) -> User | None:
    token = request.cookies.get(COOKIE_NAME)
    if not token:
        return None
    payload = decode_token(token)
    if not payload:
        return None
    db: Session = SessionLocal()
    try:
        user = db.query(User).filter(User.id == int(payload["sub"])).first()
        return user
    finally:
        db.close()


def require_login(request: Request) -> User | None:
    user = get_current_user(request)
    if user is None:
        return RedirectResponse(url="/login", status_code=302)
    return user
