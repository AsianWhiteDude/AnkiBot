import asyncio
import logging

from aiogram import Bot, Dispatcher


from config.config import Config, PostgreConfig, load_config, load_database
from handlers import (create_set_handlers, command_handlers,
                      other_handlers, all_sets_handlers,
                      add_card_handlers, study_cards)
from keyboards.main_menu import set_main_menu
from database.base import BaseModel
from database.engine import (create_async_engine,
                             proceed_schemas, get_session_maker)
from middlewares.register_check import register_check
from aiogram.fsm.storage.redis import RedisStorage
from structures.redis import redis

async def main():

    #Initializing logger:
    logger = logging.getLogger(__name__)

    #Setting basic config for logger
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
                '[%(asctime)s] - %(name)s - %(message)s')

    logger.info("Starting bot!")

    config_bot: Config = load_config()
    config_db: PostgreConfig = load_database()

    #Initialization of bot and dispatcher
    bot = Bot(token=config_bot.tg_bot.token, parse_mode="HTML")

    storage = RedisStorage(redis=redis)

    dp = Dispatcher(storage=storage)

    #Setting main menu for commands
    await set_main_menu(bot)

    async_engine = create_async_engine(config_db.POSTGRES_URL)
    session_maker = get_session_maker(async_engine)
    await proceed_schemas(async_engine, BaseModel.metadata)

    dp.workflow_data.update({'session_maker': session_maker})

    #Connecting routers from handlers

    dp.include_router(all_sets_handlers.router)
    dp.include_router(add_card_handlers.router)
    dp.include_router(study_cards.router)
    dp.include_router(create_set_handlers.router)
    dp.include_router(command_handlers.router)
    dp.include_router(other_handlers.router)

    dp.message.middleware(register_check())

    #Start for only new updates
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, session_maker=session_maker)



if __name__ == "__main__":
    asyncio.run(main())