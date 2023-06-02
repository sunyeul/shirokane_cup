from database import engine, get_db
from models import SubmitStore
from datetime import datetime
from utils import format_time_ago

import pandas as pd


# データベース周りの関数たち
def insert_submission(
    competition_id: str,
    user_id: int = None,
    description: str = None,
    score: float = None,
):
    nowtime = datetime.now()

    c2 = SubmitStore(
        competition_id=competition_id,
        user_id=user_id,
        description=description,
        score=score,
        upload_date=nowtime,
    )
    # Use get_db to obtain a session
    session_gen = get_db()
    session = next(session_gen)

    session.add(c2)
    session.commit()


def read_leaderboard(competition_id: int) -> pd.DataFrame:
    # 特定のコンペの全ての提出データを取得するためのSQLクエリ
    query = f"""
        SELECT
            "rank" AS "Rank",
            users.username AS "Username", 
            MIN(submissions.score) AS "Best Score",
            COUNT(submissions.id) AS "#Submission", 
            MAX(submissions.upload_date) AS "Last Submission"
        FROM 
            submissions 
        INNER JOIN 
            users ON users.id = submissions.user_id
        WHERE
            submissions.competition_id = {competition_id}
        GROUP BY 
            users.username 
        ORDER BY 
            "Best Score" ASC
    """

    leaderboard: pd.DataFrame = pd.read_sql_query(query, engine)

    # 'Last Submission'列をより人間が読みやすい時間形式に更新
    leaderboard["Last Submission"] = format_time_ago(leaderboard["Last Submission"])
    print(leaderboard)

    return leaderboard


def read_my_submissions(competition_id: id, username: str) -> pd.DataFrame:
    query = f"""
    SELECT
        description AS "Description",
        score AS "Score",
        upload_date AS "Upload Date",
        upload_date AS "Last Submission"
    FROM
        submissions
    INNER JOIN 
            users ON users.id = submissions.user_id
    WHERE
        submissions.competition_id = {competition_id}
        AND users.username = "{username}"
    ORDER BY
        upload_date DESC
    """

    my_submissions: pd.DataFrame = pd.read_sql_query(query, engine)
    my_submissions["Last Submission"] = format_time_ago(
        my_submissions["Last Submission"]
    )

    return my_submissions
