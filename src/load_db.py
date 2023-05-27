from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import pandas as pd
from datetime import datetime


def load_db(compe, sort_column, display_column, sort_ascending) -> pd.DataFrame:
    engine = create_engine(
        "sqlite:///competitions/" + compe + "/db/submission.db", echo=False
    )

    tbl_score = pd.read_sql_query("SELECT * FROM score ORDER BY " + sort_column, engine)
    tbl_submit = pd.read_sql_query("SELECT * FROM submit", engine)

    tbl_merged = pd.merge(
        tbl_score, tbl_submit[["id", "upload_date"]], on="id", how="inner"
    )

    # convert datetime into strings such as "XX month ago", or "XX minitues ago".
    def convert_time(t):
        time = datetime.strptime(t, "%Y-%m-%d %H:%M:%S.%f")
        diff = datetime.now() - time

        passed_list = [
            diff.days // 30,
            diff.days,
            diff.seconds // 3600,
            diff.seconds // 60,
        ]

        accessory = ["mo", "d", "hr", "min"]

        passed = "now"
        for p, a in zip(passed_list, accessory):
            if p == 0:
                pass
            else:
                passed = "{}{}{}".format(p, a, "s" if a == "hr" and p > 1 else "")
                break

        return passed

    tbl_merged["upload_date"] = tbl_merged["upload_date"].map(convert_time)

    # generate entry count
    s = tbl_merged.groupby("user_id").agg({"id": "count"}).reset_index()
    tbl_merged = pd.merge(
        tbl_merged, s.rename({"id": "entry"}, axis=1), on="user_id", how="left"
    )

    # leave top score each user
    # top_scores_index = np.ravel(tbl_merged.groupby("user_id").agg({"total_click": np.argmax}))
    # tbl_merged = tbl_merged.iloc[top_scores_index]

    # align columns order
    tbl_merged = tbl_merged[
        ["title", "user_id", sort_column] + display_column + ["entry", "upload_date"]
    ]

    return tbl_merged.sort_values(sort_column, ascending=sort_ascending)
