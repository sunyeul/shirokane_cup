from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from jinja2 import FileSystemLoader
from load_db import load_db

import importlib


router = APIRouter()
templates = Jinja2Templates(directory="templates")
templates.env.loader = FileSystemLoader(["./templates", "./competitions"])


@router.get("/leaderboard", response_class=HTMLResponse)
async def leaderboard_page(request: Request, compe: str):
    ScoreCalculator = importlib.import_module(
        "competitions." + compe + ".src.ScoreCalculator"
    )

    sc = ScoreCalculator.ScoreCalculator(
        "./competitions/" + compe + "/data/true_answer.pkl"
    )
    db = load_db(compe, sc.main_score, sc.disp_score, sc.ascending)

    return templates.TemplateResponse(
        "leaderboard.html", {"request": request, "tables": db, "compe": compe}
    )
