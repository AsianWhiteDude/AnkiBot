from typing import Any, Awaitable, Callable, Dict, Union
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from sqlalchemy import select
from database.engine import sessionmaker
from database.user import User
from database.db_commands import is_user_exists
from structures.redis import redis


class register_check(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Union[Message, CallbackQuery],
        data: Dict[str, Any]
    ) -> Any:

        session_maker: sessionmaker = data['session_maker']

        if is_user_exists(user_id=event.from_user.id, session_maker=session_maker, redis=redis):
            return await handler(event, data)

        async with session_maker() as session:
            async with session.begin():
                user = User(
                    user_id=event.from_user.id,
                    username=event.from_user.username,
                )
                await session.merge(user)
                if isinstance(event, Message):
                    await event.answer('Ты был успешно зарегестрирован!')
                else:
                    await event.message.answer('Ты был успешно зарегестрирован!')

        return await handler(event, data)
