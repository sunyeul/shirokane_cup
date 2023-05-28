from sqlalchemy import Column, Integer, String
from database import Base


class User(Base):
    __tablename__ = "user"

    user_id = Column("user_id", Integer, primary_key=True)
    username = (Column("username", String),)
    hashed_password = (Column("hashed_password", String),)
