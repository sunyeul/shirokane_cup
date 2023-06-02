from fastapi import APIRouter, Request, UploadFile, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from jinja2 import FileSystemLoader

from data_check import FileCheckError
from typing import Annotated
from compe_db import (
    insert_submission,
    read_leaderboard,
)

from auth import get_current_user

import io
import importlib
import pandas as pd

from database import get_db


router = APIRouter()
templates = Jinja2Templates(directory="templates")
templates.env.loader = FileSystemLoader(["./templates", "./competitions"])


@router.get("/submit", response_class=HTMLResponse)
async def submit_page(request: Request, compe: str, db=Depends(get_db)):
    try:
        _ = await get_current_user(request, db)
    except:
        return RedirectResponse(url="/login", status_code=302)

    return templates.TemplateResponse(
        "submit.html",
        {"request": request, "macro_src": f"./{compe}/templates/macro.html"},
    )


@router.post("/submitresult")
async def submitresult(
    request: Request,
    compe: str,
    upload_file: UploadFile,
    description: Annotated[str, Form()],
    db=Depends(get_db),
):
    # Convert submitted file to data frame
    try:
        file_content = await upload_file.read()
        file_like_object = io.BytesIO(file_content)
        df_submit = pd.read_csv(file_like_object)
    except (ValueError, UnicodeDecodeError):
        msg = "submitted file failed to convert to data frame. Please check."
        return templates.TemplateResponse(
            "submit.html",
            {
                "request": request,
                "macro_src": f"./{compe}/templates/macro.html",
                "msg": msg,
            },
        )

    # TODO: Save the sumbitted file to the database

    # calculate score
    compe_module = importlib.import_module("competitions." + compe)

    try:
        sc = compe_module.score_calculator
        score = sc.calc_score(df_submit)
    except FileCheckError as e:
        return templates.TemplateResponse(
            "submit.html",
            {
                "request": request,
                "macro_src": f"./{compe}/templates/macro.html",
                "msg": e.message,
            },
        )

    # add file contents and upload information into database
    user = await get_current_user(request, db)
    insert_submission(
        competition_id=int(compe),
        user_id=user.id,
        description=description,
        score=score,
    )

    # update leaderboard
    leaderboard = read_leaderboard(compe)

    return templates.TemplateResponse(
        "leaderboard.html",
        {
            "request": request,
            "tables": leaderboard,
            "main_score": score,
            "compe": compe,
            "macro_src": f"./{compe}/templates/macro.html",
        },
    )
