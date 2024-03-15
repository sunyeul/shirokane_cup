from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from crud import read_leaderboard


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/leaderboard", response_class=HTMLResponse)
async def leaderboard_page(request: Request):
    leaderboard = read_leaderboard()
    return templates.TemplateResponse(
        "leaderboard.html",
        {
            "request": request,
            "tables": leaderboard,
            "macro_src": "macro.html",
        },
    )
