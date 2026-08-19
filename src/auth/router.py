from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from src.auth.dependencies import COOKIE_NAME, create_token, get_current_user
from src.auth.password import verify_password
from src.config.settings import settings
from src.storage.database import SessionLocal
from src.storage.models import User

router = APIRouter()


def _get_templates():
    from fastapi.templating import Jinja2Templates
    from pathlib import Path
    return Jinja2Templates(directory=Path(__file__).resolve().parent.parent / "templates")


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    user = get_current_user(request)
    if user:
        return RedirectResponse(url="/dashboard", status_code=302)
    tmpl = _get_templates()
    return tmpl.TemplateResponse(request, "login.html", {"error": None})


@router.post("/login")
async def login_submit(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
):
    tmpl = _get_templates()
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if not user or not verify_password(password, user.password_hash):
            return tmpl.TemplateResponse(request, "login.html", {
                "error": "Credenciais invalidas",
            })
        token = create_token(user.id, user.username)
        response = RedirectResponse(url="/dashboard", status_code=302)
        response.set_cookie(
            COOKIE_NAME,
            token,
            httponly=True,
            samesite="lax",
            max_age=settings.jwt_expire_hours * 3600,
        )
        return response
    finally:
        db.close()


@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie(COOKIE_NAME)
    return response
