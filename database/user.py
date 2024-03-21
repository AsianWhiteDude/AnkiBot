import datetime

from sqlalchemy import Column, Integer, DATE, VARCHAR
from sqlalchemy.dialects.postgresql import JSONB

from .base import BaseModel

class User(BaseModel):
    __tablename__ = 'users'

    user_id = Column(Integer, unique=True, nullable=False, primary_key=True) # Telegram user id

    username = Column(VARCHAR(32), unique=False, nullable=True)

    data = Column(JSONB)

    reg_date = Column(DATE, default=datetime.date.today())

    upd_date = Column(DATE, onupdate=datetime.date.today())

    def __str__(self):
        return f'<User:{self.user_id}>'