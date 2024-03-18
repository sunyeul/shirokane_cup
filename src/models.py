from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    display_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)

    # relationships
    submissions = relationship("SubmitStore", back_populates="user")
    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="user")


class SubmitStore(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    description = Column(String(100), nullable=False)
    score = Column(Float, nullable=False)
    upload_date = Column(DateTime, nullable=False, default=datetime.now)

    # relationships
    user = relationship("User", back_populates="submissions")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    upvotes = Column(Integer, default=0)
    created_at = Column(DateTime, nullable=False, default=datetime.now)

    # relationships
    user = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))
    created_at = Column(DateTime, nullable=False, default=datetime.now)

    # relationships
    post = relationship("Post", back_populates="comments")
    user = relationship("User", back_populates="comments")
