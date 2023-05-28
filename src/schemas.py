from datetime import date
from pydantic import BaseModel


class User(BaseModel):
    user_id: int
    username: str
    hashed_password: str

    class Config:
        orm_mode = True
