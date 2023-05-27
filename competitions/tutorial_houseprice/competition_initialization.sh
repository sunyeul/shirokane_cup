#!/usr/bin/bash

# 既存テーブルのバックアップ
if [ -e db/submission.db ]; then
  mkdir -p backup
  sqlite3 db/submission.db < sql/make_backup.sql 
  rm db/submission.db
fi

# 新規作成
sqlite3 db/submission.db < sql/create_table.sql
