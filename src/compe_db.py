from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from datetime import datetime
from importlib import import_module
from utils import format_time_ago

import pandas as pd


# データベース周りの関数たち
def insert_compe_submission_tbl(
    compe: str,
    user_id: int = None,
    username: str = None,
    description: str = None,
    score: float = None,
):
    engine = create_engine(
        "sqlite:///competitions/" + compe + "/db/submission.db", echo=False
    )
    session = sessionmaker(bind=engine)()

    compe_module = import_module("competitions." + compe)
    models = compe_module.models
    nowtime = datetime.now()

    c2 = models.SubmitStore(
        user_id=user_id,
        username=username,
        description=description,
        score=score,
        upload_date=nowtime,
    )
    session.add(c2)
    session.commit()


def update_compe_leaderboard_tbl(compe):
    engine = create_engine(
        "sqlite:///competitions/" + compe + "/db/submission.db", echo=False
    )

    tbl_submit = pd.read_sql_query("SELECT * FROM submission", engine)
    leaderboard = (
        tbl_submit.groupby("username", as_index=False)
        .agg({"score": "min", "submission_id": "count", "upload_date": "max"})
        .sort_values("score", ascending=False)
        .reset_index(drop=True)
        .reset_index()
        .rename(
            columns={
                "index": "rank",
                "score": "best score",
                "submission_id": "#submission",
            }
        )
    )
    leaderboard.to_sql("leaderboard", engine, if_exists="replace", index=False)


def read_compe_leaderboard_tbl(compe: str) -> pd.DataFrame:
    engine = create_engine(
        "sqlite:///competitions/" + compe + "/db/submission.db", echo=False
    )

    leaderboard_tbl = pd.read_sql_query("SELECT * FROM leaderboard", engine)
    leaderboard_tbl["upload_date"] = format_time_ago(leaderboard_tbl["upload_date"])
    leaderboard_tbl.rename(
        columns={
            "rank": "Rank",
            "username": "Username",
            "best score": "Best Score",
            "#submission": "#Submission",
            "upload_date": "Last Submission",
        },
        inplace=True,
    )

    return leaderboard_tbl


def read_compe_submission_tbl(compe: str) -> pd.DataFrame:
    engine = create_engine(
        "sqlite:///competitions/" + compe + "/db/submission.db", echo=False
    )

    submission_tbl = pd.read_sql_query("SELECT * FROM submission", engine)
    submission_tbl["last_submission"] = format_time_ago(submission_tbl["upload_date"])

    return submission_tbl
