
from typing import Any, Awaitable, Callable, Dict, Union

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from sqlalchemy import select

from database.engine import sessionmaker


from database.user import User


#Initializing "data base" actually just a dict
#Later should be implemented in SQL
users_db: dict[int, dict[str, dict[str, str]]] = {}


