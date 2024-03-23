
from typing import Callable, Dict, Any, Awaitable, Union

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, TelegramObject

from database.db_commands import is_user_exists, create_user

class register_check(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Union[Message, CallbackQuery],
        data: Dict[str, Any]
    ) -> Any:

        if event.web_app_data:
            return await handler(event, data)

        session_maker = data['session_maker']
        redis = data['redis']
        result = await is_user_exists(user_id=event.from_user.id, session_maker=session_maker, redis=redis)
        print(result)

        if not result:
            await create_user(user_id=event.from_user.id,
                              username=event.from_user.username, session_maker=session_maker)
            await data['bot'].send_message(event.from_user.id, 'Ты успешно зарегистрирован(а)!')

        return await handler(event, data)

