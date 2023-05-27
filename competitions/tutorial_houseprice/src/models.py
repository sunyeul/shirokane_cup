# model declearation

from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class ScoreStore(Base):
    __tablename__ = "score"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    title = Column(String(128))
    RMSLE = Column(Float)

    def __init__(self, title, user_id, **args):
        self.title = title
        self.user_id = user_id
        self.RMSLE = args["RMSLE"]

    def __repr__(self):
        return "<Title {}>".format(self.title)


class SubmitStore(Base):
    __tablename__ = "submit"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    title = Column(String(128))
    upload_date = Column(DateTime)
    raw_text = Column(String(1024**2))  # Approx. 1 million chars.

    def __init__(self, title=None, user_id=None, upload_date=None, raw_text=None):
        self.title = title
        self.user_id = user_id
        self.upload_date = upload_date
        self.raw_text = raw_text

    def __repr__(self):
        return "<Title {}>".format(self.title)
