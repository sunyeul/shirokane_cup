#!/usr/bin/bash

# 既存テーブルのバックアップ
if [ -e db/shirokane_cup.db ]; then
  mkdir -p data/backup
  sqlite3 db/shirokane_cup.db < sql/make_backup.sql 
  rm db/shirokane_cup.db
fi

# 新規作成
sqlite3 db/shirokane_cup.db < sql/create_tables.sql
