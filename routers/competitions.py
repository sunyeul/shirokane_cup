from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from jinja2 import FileSystemLoader

from auth import get_current_active_user, UserInDB

import os

router = APIRouter()
templates = Jinja2Templates(directory="templates")
templates.env.loader = FileSystemLoader(["./templates", "./competitions"])


@router.get(
    "/competitions",
    response_class=HTMLResponse,
    dependencies=[Depends(get_current_active_user)],
)
async def top_page(request: Request):
    competition_links = [
        {"href": f"/competitions/{compe}/overview", "name": compe}
        for compe in os.listdir("./competitions")
    ]
    return templates.TemplateResponse(
        "competitions.html",
        {"request": request, "competition_links": competition_links},
    )
