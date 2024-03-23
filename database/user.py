import datetime

from sqlalchemy import Column, Integer, DATE, VARCHAR, ForeignKey, Text, BigInteger
from sqlalchemy.dialects.postgresql import JSONB

from .base import BaseModel

class User(BaseModel):
    __tablename__ = 'users'

    user_id = Column(BigInteger, unique=True, nullable=False, primary_key=True) # Telegram user id

    username = Column(VARCHAR(32), unique=False, nullable=True)

    reg_date = Column(DATE, default=datetime.date.today())

    upd_date = Column(DATE, onupdate=datetime.date.today())

    def __str__(self):
        return f'<User:{self.user_id}>'


class Deck(BaseModel):
    __tablename__ = 'decks'

    deck_id = Column(BigInteger, unique=True, nullable=False, primary_key=True, autoincrement=True)

    deck_name = Column(VARCHAR(32), unique=True, nullable=False)

    user_id = Column(ForeignKey('users.user_id'))

    def __str__(self):
        return f'<Deck:{self.deck_id}>'


class Card(BaseModel):
    __tablename__ = 'cards'

    card_id = Column(BigInteger, unique=True, nullable=False, primary_key=True, autoincrement=True)

    card_front = Column(Text, unique=True, nullable=False)

    card_back = Column(Text, unique=False, nullable=False)

    deck_id = Column(ForeignKey('decks.deck_id'))

    def __str__(self):
        return f'<Card:{self.card_id}>'