from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True)
    username = Column("username", String)
    hashed_password = Column("hashed_password", String)

    def __init__(
        self,
        id: int,
        username: str,
        hashed_password: str,
    ):
        self.id = id
        self.username = username
        self.hashed_password = hashed_password


class Competition(Base):
    __tablename__ = "competitions"

    id = Column("id", Integer, primary_key=True)
    title = Column("title", String)
    subtitle = Column("subtitle", String)
    description = Column("description", String)


class SubmitStore(Base):
    __tablename__ = "submissions"
    id = Column(Integer, primary_key=True)
    competition_id = Column(Integer, ForeignKey("competitions.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    description = Column(String(100))
    score = Column(Float)
    upload_date = Column(DateTime)

    def __init__(
        self,
        competition_id: int = None,
        user_id: int = None,
        description: str = None,
        score: float = None,
        upload_date=None,
    ):
        self.competition_id = competition_id
        self.user_id = user_id
        self.description = description
        self.score = score
        self.upload_date = upload_date
