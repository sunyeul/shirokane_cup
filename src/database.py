import os

from sqlalchemy import MetaData, create_engine, Table, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from databases import Database

USER_DATABASE_URL = "sqlite:///./db/user.db"
engine = create_engine(USER_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

metadata = MetaData()
metadata.create_all(engine)

user_table = Table(
    "user",
    metadata,
    Column("user_id", Integer, primary_key=True),
    Column("username", String),
    Column("hashed_password", String),
)

user_database = Database(USER_DATABASE_URL)
