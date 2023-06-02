from dataclasses import dataclass, field
from typing import Dict, List, Tuple

import pandas as pd


@dataclass(frozen=True)
class Check:
    func: callable  # 検証するための関数
    error: Exception  # 検証で失敗した場合に投げる例外


@dataclass(frozen=True)
class Column:
    dtype: type  # データ型
    unique: bool = False  # ユニークな値のみ許可するかどうか
    not_null: bool = False  # NULLを許可しないかどうか
    checks: List[Check] = field(default_factory=list)  # 列に適用するチェックのリスト


@dataclass(frozen=True)
class Schema:
    columns: Dict[str, Column]  # 列名とColumnオブジェクトの辞書
    size: Tuple[int, int]  # データフレームの望ましいサイズ (行数, 列数)
    primary_key: List[str]  # プライマリキーのリスト
    strict: bool = (True,)  # このフラグがTrueの場合、データフレームはスキーマで定義された列のみを持つ必要があります
    checks: List[Check] = field(default_factory=list)  # データフレーム全体に適用するチェックのリスト


class SchemaChecker:
    def __init__(self, schema: Schema):
        self.schema = schema
        self.error_msgs = []

    def check_size(self, df: pd.DataFrame):
        # データフレームのサイズの検証
        if df.shape != self.schema.size:
            error_msg = (
                f"望ましいデータサイズは{self.schema.size}ですが、あなたが提出したデータのサイズは{df.shape}です。"
            )
            self.error_msgs.append(error_msg)

    def check_column_name(self, df: pd.DataFrame):
        # 列名の検証
        if sorted(df.columns) != sorted(self.schema.columns.keys()):
            error_msg = "あなたが提出したデータの列名が間違っています。"
            self.error_msgs.append(error_msg)

    def check_data_type(self, df: pd.DataFrame):
        # データ型の検証
        for c in df.columns:
            if df[c].dtype != self.schema.columns[c].dtype:
                error_msg = "あなたが提出したデータは、望ましい{c}の型は{self.schema.columns[c].dtype}ですが、{df[c].dtype}になっています。"
                self.error_msgs.append(error_msg)

    def check_unique(self, df: pd.DataFrame):
        for column, properties in self.schema.columns.items():
            if properties.unique and df[column].duplicated().any():
                error_msg = f"あなたが提出したデータの{column}列に重複する値があります。"
                self.error_msgs.append(error_msg)

    def check_primary_key(self, df: pd.DataFrame):
        if df[self.schema.primary_key].duplicated().any():
            error_msg = f"あなたが提出したデータの{self.schema.primary_key}主キーに重複する値があります。"
            self.error_msgs.append(error_msg)

    def check_null(self, df: pd.DataFrame):
        # NULLの存在を検証
        for column, properties in self.schema.columns.items():
            if properties.not_null and df[column].isna().any():
                error_msg = "あなたが提出したデータの{column}列に欠損値が存在します。"
                self.error_msgs.append(error_msg)

    def check_custom_constraints(self, df: pd.DataFrame):
        # カスタムの制約条件を検証
        for column, properties in self.schema.columns.items():
            for check in properties.checks:
                if not check.func(df[column]):
                    self.error_msgs.append(check.error.format(column))

        for check in self.schema.checks:
            if not check.func(df):
                self.error_msgs.append(check.error)

    def run_all_checks(self, df):
        # 全ての検証を実行
        # 1. データフレームのサイズを検証
        self.check_size(df)
        # 2. 列名を検証
        self.check_column_name(df)
        # 3. データ型を検証
        self.check_data_type(df)
        # 4. NULLの存在を検証
        self.check_null(df)
        # 5. 主キーの重複を検証
        self.check_primary_key(df)
        # 6. 各列の重複を検証
        self.check_unique(df)
        # 7. ユーザー定義の制約条件を検証
        self.check_custom_constraints(df)

        # エラーメッセージが存在する場合は例外を発生
        if len(self.error_msgs) > 0:
            raise FileCheckError("\n".join(self.error_msgs))


# 独自定義例外
class FileCheckError(Exception):
    "提出ファイルが正しいかどうかのチェックポイントに関する基底エラー"
    pass
