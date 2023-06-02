from pathlib import Path

from data_check import Schema, Column
from score import Score, ScoreCalculator

import numpy as np


# コンペメタデータ
competition_title = "【テストコンペ】住宅価格予測コンペ"
competition_subtitle = "住宅価格を予測しよう"

# ディレクトリ経路の取得
PWD = Path(__file__).resolve().parent

data_file_path = PWD / "data/data.zip"
ans_data_path = PWD / "data/true_answer.csv"
macro_src_path = PWD / "templates/macro.html"

# 正解データのスキーマ
answer_schema = Schema(
    columns={
        "Id": Column(np.int64, unique=True, not_null=True),
        "TruePrice": Column(np.int64, not_null=True),
    },
    primary_key=["Id"],
    size=(292, 2),
)

# 提出データのスキーマ
submission_schema = Schema(
    columns={
        "Id": Column(np.int64, unique=True, not_null=True),
        "SalePrice": Column(np.int64, not_null=True),
    },
    primary_key=["Id"],
    size=(292, 2),
)


# 評価指標の定義
def calc_rmsle(actual, predict):
    msle = ((np.log(actual + 1) - np.log(predict + 1)) ** 2).sum() / len(actual)
    rmsle = msle**1 / 2
    return rmsle


rmsle = Score(
    name="RMSLE",
    merge_on=["Id"],
    merge_how="inner",
    true_column="TruePrice",
    pred_column="SalePrice",
    score_func=calc_rmsle,
    greater_is_better=False,
    description="Root Mean Squared Logarithmic Error",
)

score_calculator = ScoreCalculator(
    ans_data_path=ans_data_path,
    answer_schema=answer_schema,
    submission_schema=submission_schema,
    score=rmsle,
)
