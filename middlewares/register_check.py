from typing import Any, Awaitable, Callable, Dict, Union

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from sqlalchemy import select

from database.engine import sessionmaker


from database.user import User


class register_check(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Union[Message, CallbackQuery],
        data: Dict[str, Any]
    ) -> Any:

        session_maker: sessionmaker = data['session_maker']
        async with session_maker() as session:
            async with session.begin():
                result = await session.execute(statement=select(User).where(User.user_id == event.from_user.id))
                user = result.one_or_none()

                if user:
                    pass
                else:
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
