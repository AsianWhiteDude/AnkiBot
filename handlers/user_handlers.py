from aiogram import F, Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import CallbackQuery, Message
from database.database import users_db
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from keyboards.reply_menu import sets_cards_kb

from lexicon.lexicon_ru import LEXICON


router = Router()


class FSMAddSet(StatesGroup):

    fill_name = State()


class FSMAddCard(StatesGroup):

    fill_front = State()
    fill_back = State()


# Этот хэндлер будет срабатывать на команду "/start" -
# добавлять пользователя в базу данных, если его там еще не было
# и отправлять ему приветственное сообщение
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(LEXICON[message.text], reply_markup=sets_cards_kb)

    if message.from_user.id not in users_db:
        users_db[message.from_user.id] = {}


# Этот хэндлер будет срабатывать на команду "/help"
# и отправлять пользователю сообщение со списком доступных команд в боте
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(LEXICON[message.text], reply_markup=sets_cards_kb)

# Этот хэндлер будет срабатывать на команду "/cancel" в любых состояниях,
# кроме состояния по умолчанию, и отключать машину состояний
@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(LEXICON[message.text], reply_markup=sets_cards_kb)
    await state.clear()


@router.message(F.text == LEXICON['button_add_set'], StateFilter(default_state))
async def process_fillname(message: Message, state: FSMContext):
    await message.answer(text='Пожалуйста, введите название сета:')
    # Устанавливаем состояние ожидания ввода имени
    await state.set_state(FSMAddSet.fill_name)

@router.message(StateFilter(FSMAddSet.fill_name), F.text.isalpha())
async def process_fillname_sent(message: Message, state: FSMContext):
    await state.update_data(name=message.text)

    users_db[message.from_user.id][message.text] = {}

    await message.answer(text=f'Отлично! Сет с именем {message.text} был успешно создан', reply_markup=sets_cards_kb)

# Этот хэндлер будет срабатывать, если во время ввода имени
# будет введено что-то некорректное
@router.message(StateFilter(FSMAddSet.fill_name))
async def warning_not_name(message: Message):
    await message.answer(
        text='То, что вы отправили не похоже на название\n\n'
             'Пожалуйста, введите название сета\n\n'
             'Если вы хотите прервать заполнение анкеты - '
             'отправьте команду /cancel'
    )
