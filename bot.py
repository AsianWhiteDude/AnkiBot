import asyncio
import logging

from aiogram import Bot, Dispatcher
from config.config import Config, load_config
from handlers import (create_set_handlers, command_handlers,
                      other_handlers, all_sets_handlers,
                      add_card_handlers)
from keyboards.main_menu import set_main_menu



async def main():

    #Initializing logger:
    logger = logging.getLogger(__name__)

    #Setting basic config for logger
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
                '[%(asctime)s] - %(name)s - %(message)s')

    logger.info("Starting bot!")

    config: Config = load_config()

    #Initialization of bot and dispatcher
    bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    dp = Dispatcher()

    #Setting main menu for commands
    await set_main_menu(bot)

    #Connecting routers from handlers
    dp.include_router(command_handlers.router)
    dp.include_router(all_sets_handlers.router)
    dp.include_router(add_card_handlers.router)
    dp.include_router(create_set_handlers.router)
    dp.include_router(other_handlers.router)

    #Start for only new updates
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())