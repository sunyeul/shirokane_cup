from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from jinja2 import FileSystemLoader
from load_db import load_db

import importlib
from auth import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="templates")
templates.env.loader = FileSystemLoader(["./templates", "./competitions"])


@router.get("/mysubmission", response_class=HTMLResponse)
async def mysub_page(request: Request, compe: str):
    try:
        _ = await get_current_user(request)
    except:
        return RedirectResponse(url="/login", status_code=302)

    ScoreCalculator = importlib.import_module(
        "competitions." + compe + ".src.ScoreCalculator"
    )
    sc = ScoreCalculator.ScoreCalculator(
        "./competitions/" + compe + "/data/true_answer.pkl"
    )
    db = load_db(compe, sc.main_score, sc.disp_score, sc.ascending)

    return templates.TemplateResponse(
        "mysubmission.html",
        {"request": request, "tables": db, "macro_src": "./" + compe + "/macro.html"},
    )
