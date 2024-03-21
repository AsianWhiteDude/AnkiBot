from typing import Any, Awaitable, Callable, Dict, Union

from aiogram.types import TelegramObject, Message, CallbackQuery
from sqlalchemy import select

from database.engine import sessionmaker


from database.user import User



async def add_set(user_id: int, set_name: str, session_maker: sessionmaker) -> None:

    json_data = {set_name: '{}'}

    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(
                statement=User.insert().values(
                data=json_data).where(User.user_id==user_id)
                                           )


async def add_card(user_id: int, card: [str, str], session_maker: sessionmaker) -> None:
    json_data = card

    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(
                statement=User.insert().values(
                data=json_data).where(User.user_id==user_id)
                                           )

