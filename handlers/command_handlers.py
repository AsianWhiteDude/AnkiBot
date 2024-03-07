
from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from database.database import users_db
from keyboards.reply_menu import sets_cards_kb
from lexicon.lexicon_ru import LEXICON
from all_sets_handlers import process_all_sets
from add_card_handlers import process_choose_set
from create_set_handlers import process_enter_name


router = Router()


# This handler is triggered when user starts the bot
# and registers user in the 'data base'
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(LEXICON[message.text], reply_markup=sets_cards_kb)

    if message.from_user.id not in users_db:
        users_db[message.from_user.id] = {}


# This handler is triggered when user enters command "/help"
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(LEXICON[message.text], reply_markup=sets_cards_kb)


# This handler is triggered when user enters command "/cancel"
@router.message(Command(commands='cancel'))
async def process_cancel_command(message: Message):
    await message.answer(LEXICON[message.text], reply_markup=sets_cards_kb)

# This handler is triggered when user enters command "/sets"
@router.message(Command(commands='sets'))
async def process_set_command(message: Message):
    await process_all_sets(message)

# This handler is triggered when user enters command "/addset"
@router.message(Command(commands='addset'))
async def process_set_command(message: Message):
    await process_enter_name(message)

# This handler is triggered when user enters command "/addcard"
@router.message(Command(commands='addcard'))
async def process_set_command(message: Message):
    await process_choose_set(message)
