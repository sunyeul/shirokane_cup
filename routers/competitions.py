from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from jinja2 import FileSystemLoader

import os

router = APIRouter()
templates = Jinja2Templates(directory="templates")
templates.env.loader = FileSystemLoader(["./templates", "./competitions"])


@router.get(
    "/competitions",
    response_class=HTMLResponse,
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
