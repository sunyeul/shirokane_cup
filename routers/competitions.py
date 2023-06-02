from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from jinja2 import FileSystemLoader

import os

from importlib import import_module

router = APIRouter()
templates = Jinja2Templates(directory="templates")
templates.env.loader = FileSystemLoader(["./templates", "./competitions"])


@router.get(
    "/competitions",
    response_class=HTMLResponse,
)
async def top_page(request: Request):
    competition_links = []

    for compe in os.listdir("./competitions"):
        competition_link = {}
        competition_link["href"] = f"/competitions/{compe}/overview"

        compe_module = import_module(f"competitions.{compe}")
        competition_link["name"] = compe_module.competition_title

        competition_links.append(competition_link)

    return templates.TemplateResponse(
        "competitions.html",
        {"request": request, "competition_links": competition_links},
    )
