
from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message
from sqlalchemy.orm import sessionmaker

from handlers.study_cards import process_study_set
from keyboards.reply_menu import sets_cards_kb
from lexicon.lexicon_ru import LEXICON
from handlers.all_sets_handlers import process_all_sets
from handlers.add_card_handlers import process_choose_set
from handlers.create_set_handlers import process_enter_name
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

router = Router()


# This handler is triggered when user starts the bot
# and registers user in the 'data base'
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(LEXICON[message.text], reply_markup=sets_cards_kb)


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
async def process_set_command(message: Message, session_maker: sessionmaker):
    await process_all_sets(message, session_maker)

# This handler is triggered when user enters command "/addset"
@router.message(Command(commands='addset'), StateFilter(default_state))
async def process_set_command(message: Message, state: FSMContext):
    await process_enter_name(message, state)

# This handler is triggered when user enters command "/addcard"
@router.message(Command(commands='addcard'), StateFilter(default_state))
async def process_set_command(message: Message, state: FSMContext, session_maker: sessionmaker):
    await process_choose_set(message, state, session_maker)


@router.message(Command(commands='studyset'), StateFilter(default_state))
async def process_set_command(message: Message, session_maker: sessionmaker):
    await process_study_set(message, session_maker)
