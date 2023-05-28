from fastapi import APIRouter, Request, UploadFile, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from jinja2 import FileSystemLoader

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from datetime import datetime
from typing import Annotated
from load_db import load_db

import io
import importlib
import pandas as pd


router = APIRouter()
templates = Jinja2Templates(directory="templates")
templates.env.loader = FileSystemLoader(["./templates", "./competitions"])


@router.post("/submitresult")
async def submitresult(
    request: Request,
    compe: str,
    submit_name: Annotated[str, Form()],
    user_name: Annotated[str, Form()],
    upload_file: UploadFile,
):
    ScoreCalculator = importlib.import_module(
        "competitions." + compe + ".src.ScoreCalculator"
    )

    submit_title = submit_name

    # Convert submitted file to data frame
    try:
        file_content = await upload_file.read()
        file_like_object = io.BytesIO(file_content)
        df_submit = pd.read_csv(file_like_object)
    except (ValueError, UnicodeDecodeError):
        return HTMLResponse(
            "submitted file failed to convert to data frame. Please check. <a href='/"
            + compe
            + "/submit'>back</a>"
        )

    # calculate score
    try:
        sc, scores = get_scores(df_submit, compe)
    except ScoreCalculator.FileCheckError as e:
        return HTMLResponse(e.message + "\n <a href='/" + compe + "/submit'>back</a>")

    engine = create_engine(
        "sqlite:///competitions/" + compe + "/db/submission.db", echo=False
    )
    session = sessionmaker(bind=engine)()

    # add file contents and upload information into database
    add_submitdb(
        user_id=user_name,
        submit_title=submit_title,
        file_content=file_content,
        session=session,
        compe=compe,
    )

    # add scores into database
    add_scoredb(
        title=submit_title, user_id=user_name, session=session, compe=compe, **scores
    )

    db = load_db(compe, sc.main_score, sc.disp_score, sc.ascending)
    return templates.TemplateResponse(
        "submitresult.html",
        {
            "request": request,
            "tables": db,
            "main_score": scores[sc.main_score],
            "compe": compe,
            "macro_src": "./" + compe + "/macro.html",
        },
    )


# 処理関数たち
def get_scores(df_submit, compe):
    # コンペ特有のスコア計算モジュールを読み込み
    ScoreCalculator = importlib.import_module(
        "competitions." + compe + ".src.ScoreCalculator"
    )
    # テキストからスコアを計算する
    sc = ScoreCalculator.ScoreCalculator(
        "./competitions/" + compe + "/data/true_answer.pkl"
    )
    scores = sc.calc_score(df_submit)
    return sc, scores


# データベース周りの関数たち
def add_submitdb(user_id, submit_title, file_content, session, compe):
    models = importlib.import_module("competitions." + compe + ".src.models")
    # 提出ファイルのrow_textをデータベースに保存する
    nowtime = datetime.now()
    c2 = models.SubmitStore(
        user_id=user_id, title=submit_title, upload_date=nowtime, raw_text=file_content
    )
    session.add(c2)
    session.commit()


# def add_scoredb(title, user_id, session, compe, total_click, AUC, logloss, Accuracy, pred_click, diff):
def add_scoredb(title, user_id, session, compe, **args):
    models = importlib.import_module("competitions." + compe + ".src.models")
    # スコアをデータベースに保存する
    c = models.ScoreStore(title, user_id, **args)
    session.add(c)
    session.commit()
