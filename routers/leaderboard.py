from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from jinja2 import FileSystemLoader
from compe_db import read_compe_leaderboard_tbl

import importlib


router = APIRouter()
templates = Jinja2Templates(directory="templates")
templates.env.loader = FileSystemLoader(["./templates", "./competitions"])


@router.get("/leaderboard", response_class=HTMLResponse)
async def leaderboard_page(request: Request, compe: str):
    leaderboard = read_compe_leaderboard_tbl(compe)
    return templates.TemplateResponse(
        "leaderboard.html",
        {
            "request": request,
            "tables": leaderboard,
            "macro_src": "./" + compe + "/macro.html",
        },
    )
