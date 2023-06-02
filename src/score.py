from dataclasses import dataclass
from typing import List, Callable
from data_check import Schema, SchemaChecker, FileCheckError

import pandas as pd


@dataclass(frozen=True)
class Score:
    name: str  # スコアの名前
    merge_on: List[str]  # 結合するカラムのリスト
    merge_how: str  # 結合方法
    true_column: str  # 正解データのカラム
    pred_column: str  # 予測データのカラム
    score_func: Callable  # スコア計算関数
    greater_is_better: bool  # スコアが高い方が良いかどうか
    description: str  # スコアの説明

    def __post_init__(self):
        # 結合方法が有効な値かチェック
        valid_merge_how_values = ["left", "right", "outer", "inner"]
        if self.merge_how not in valid_merge_how_values:
            raise ValueError(
                f"merge_howの値が無効です： {self.merge_how}。期待される値： {valid_merge_how_values}。"
            )

        # スコア計算関数が呼び出し可能な関数かチェック
        if not callable(self.score_func):
            raise ValueError(
                f"score_funcの値が無効です。呼び出し可能な関数が期待されますが、{self.score_func}が得られました"
            )

    def calculate_score(self, true_df: pd.DataFrame, pred_df: pd.DataFrame) -> float:
        # 二つのデータフレームを結合してスコアを計算
        merged_df = pd.merge(true_df, pred_df, how=self.merge_how, on=self.merge_on)
        score = self.score_func(
            merged_df[self.true_column], merged_df[self.pred_column]
        )
        return score


# スコア計算用のクラス定義
class ScoreCalculator:
    df_ans_data = None

    def __init__(
        self,
        ans_data_path,
        answer_schema: Schema,
        submission_schema: Schema,
        score: Score,
    ):
        self.score = score
        self.submission_schema = submission_schema

        self.df_ans_data = self._init_answer_data(ans_data_path, answer_schema)

    def _init_answer_data(self, ans_data_path, answer_schema: Schema):
        # 回答データの読み込み
        df_ans_data = pd.read_csv(ans_data_path)

        # スキーマチェック
        try:
            SchemaChecker(answer_schema).run_all_checks(df_ans_data)
        except FileCheckError as e:
            print("Answer data does not meet the schema requirements: ", e)
            raise e

        return df_ans_data

    def calc_score(self, df_submit_data) -> dict:
        # 提出データのスキーマチェック
        try:
            SchemaChecker(self.submission_schema).run_all_checks(df_submit_data)
        except FileCheckError as e:
            raise e

        # 提出データの回答データとの一致率を計算
        score_result = self.score.calculate_score(
            true_df=self.df_ans_data,
            pred_df=df_submit_data,
        )

        return score_result
