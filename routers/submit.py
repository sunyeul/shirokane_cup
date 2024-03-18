from fastapi import APIRouter, Request, UploadFile, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from jinja2 import FileSystemLoader

from data_check import FileCheckError
from typing import Annotated
from crud import (
    insert_submission,
    read_leaderboard,
)
from score import ScoreCalculator

from auth import get_current_user

import io
import pandas as pd

from database import get_db


router = APIRouter()
templates = Jinja2Templates(directory="templates")
templates.env.loader = FileSystemLoader(["./templates", "./competition_data"])


@router.get("/submit", response_class=HTMLResponse)
async def submit_page(request: Request, db=Depends(get_db)):
    try:
        _ = await get_current_user(request, db)
    except:
        return RedirectResponse(url="/login", status_code=302)

    return templates.TemplateResponse(
        "submit.html",
        {"request": request, "macro_src": "macro.html"},
    )


@router.post("/submitresult")
async def submitresult(
    request: Request,
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
                "msg": msg,
            },
        )

    # TODO: Save the sumbitted file to the database
    # TODO: Validate submitted file
    # TODO: Calculate score

    try:
        sc = ScoreCalculator()
        score = sc.calc_score(df_submit)
    except FileCheckError as e:
        return templates.TemplateResponse(
            "submit.html",
            {
                "request": request,
                "macro_src": "macro.html",
                "msg": e.message,
            },
        )

    # add file contents and upload information into database
    user = await get_current_user(request, db)
    insert_submission(
        user_id=user.id,
        description=description,
        score=score,
    )

    # update leaderboard
    leaderboard = read_leaderboard()

    return templates.TemplateResponse(
        "leaderboard.html",
        {
            "request": request,
            "tables": leaderboard,
            "main_score": score,
            "macro_src": "macro.html",
        },
    )
