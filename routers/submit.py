from fastapi import APIRouter, Request, UploadFile, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from jinja2 import FileSystemLoader

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from typing import Annotated
from compe_db import (
    update_compe_leaderboard_tbl,
    insert_compe_submission_tbl,
    read_compe_leaderboard_tbl,
)

from auth import get_current_user

import io
import importlib
import pandas as pd


router = APIRouter()
templates = Jinja2Templates(directory="templates")
templates.env.loader = FileSystemLoader(["./templates", "./competitions"])


@router.get("/submit", response_class=HTMLResponse)
async def submit_page(request: Request, compe: str):
    try:
        _ = await get_current_user(request)
    except:
        return RedirectResponse(url="/login", status_code=302)

    return templates.TemplateResponse(
        "submit.html", {"request": request, "macro_src": "./" + compe + "/macro.html"}
    )


@router.post("/submitresult")
async def submitresult(
    request: Request,
    compe: str,
    upload_file: UploadFile,
    description: Annotated[str, Form()],
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
            {"request": request, "macro_src": "./" + compe + "/macro.html", "msg": msg},
        )

    # TODO: Save the sumbitted file to the database

    # calculate score
    compe_module = importlib.import_module("competitions." + compe)

    try:
        sc = compe_module.ScoreCalculator
        scores = sc.calc_score(df_submit)
    except compe_module.FileCheckError as e:
        return templates.TemplateResponse(
            "submit.html",
            {
                "request": request,
                "macro_src": "./" + compe + "/macro.html",
                "msg": e.message,
            },
        )

    # add file contents and upload information into database
    user = await get_current_user(request)
    insert_compe_submission_tbl(
        compe=compe,
        user_id=user.user_id,
        username=user.username,
        description=description,
        score=scores[sc.main_score],
    )

    # update leaderboard
    update_compe_leaderboard_tbl(compe)
    leaderboard = read_compe_leaderboard_tbl(compe)

    return templates.TemplateResponse(
        "leaderboard.html",
        {
            "request": request,
            "tables": leaderboard,
            "main_score": scores[sc.main_score],
            "compe": compe,
            "macro_src": "./" + compe + "/macro.html",
        },
    )
