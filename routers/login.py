from datetime import timedelta

from fastapi import APIRouter, Request, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

from auth import *
from database import get_db

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/login", response_class=HTMLResponse)
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/token", response_class=HTMLResponse)
async def login_for_access_token(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = await authenticate_user(
        username=form_data.username, password=form_data.password, db=db
    )
    if not user:
        msg = "Incorrect username or password"
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "msg": msg},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    # Set the token as a cookie in the response
    response = RedirectResponse(url="/overview", status_code=status.HTTP_302_FOUND)
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        secure=True,
        max_age=1800,
        expires=1800,
    )

    return response


@router.get("/logout")
async def logout(request: Request):
    response = templates.TemplateResponse("login.html", {"request": request})
    response.delete_cookie(key="access_token")
    return response
