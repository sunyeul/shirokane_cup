from database import engine, get_db
from models import SubmitStore, Competition
from datetime import datetime
from utils import format_time_ago

import pandas as pd


# データベース周りの関数たち
def insert_submission(
    competition_name: str,
    user_id: int = None,
    description: str = None,
    score: float = None,
):
    # Use get_db to obtain a session
    db = next(get_db())

    # get competition_id from competition_name
    competition_id = (
        db.query(Competition.id).filter(Competition.name == competition_name).scalar()
    )

    # Create a new SubmitStore object
    c2 = SubmitStore(
        competition_id=competition_id,
        user_id=user_id,
        description=description,
        score=score,
        upload_date=datetime.now(),
    )

    db.add(c2)
    db.commit()


def read_leaderboard(competition_name: int) -> pd.DataFrame:
    # 特定のコンペの全ての提出データを取得するためのSQLクエリ
    query = f"""
        SELECT
            "rank" AS "Rank",
            users.display_name AS "Username", 
            MIN(submissions.score) AS "Best Score",
            COUNT(submissions.id) AS "#Submission", 
            MAX(submissions.upload_date) AS "Last Submission"
        FROM 
            submissions 
        INNER JOIN 
            users ON users.id = submissions.user_id
        INNER JOIN 
            competitions ON competitions.id = submissions.competition_id
        WHERE
            competitions.name = "{competition_name}"
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


def read_my_submissions(competition_name: str, username: str) -> pd.DataFrame:
    query = f"""
    SELECT
        submissions.description AS "Description",
        score AS "Score",
        upload_date AS "Upload Date",
        upload_date AS "Last Submission"
    FROM
        submissions
    INNER JOIN 
        users ON users.id = submissions.user_id
    INNER JOIN 
        competitions ON competitions.id = submissions.competition_id
    WHERE
        competitions.name = "{competition_name}"
        AND users.username = "{username}"
    ORDER BY
        upload_date DESC
    """

    my_submissions: pd.DataFrame = pd.read_sql_query(query, engine)
    my_submissions["Last Submission"] = format_time_ago(
        my_submissions["Last Submission"]
    )

    return my_submissions
