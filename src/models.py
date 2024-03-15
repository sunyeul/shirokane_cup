from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from database import engine
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    display_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)

    # relationships
    submissions = relationship("SubmitStore", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, display_name={self.display_name})>"


class SubmitStore(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    description = Column(String(100), nullable=False)
    score = Column(Float, nullable=False)
    upload_date = Column(DateTime, default=datetime.utcnow, nullable=False)

    # relationships
    user = relationship("User", back_populates="submissions")

