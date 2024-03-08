from aiogram import F, Router
from aiogram.filters import  StateFilter, Command, or_f
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, CallbackQuery
from database.database import users_db
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from keyboards.reply_menu import sets_cards_kb
from keyboards.all_inline_keyboard import create_listed_inline_kb
from lexicon.lexicon_ru import LEXICON


router = Router()

# Creating state machine to keep track of a name of the set
# as well as valid name was given into handler or not
# plus stating the front and the back side of the card for
# the same reason
class FSMCard(StatesGroup):

    name_set = State()
    front = State()
    back = State()

# CBF - Callback Factory. Makes it easier to get data from
# Callbacks when you have changing data
class SetAddCBF(CallbackData, prefix='set_add'):
    set_name: str


# This handler is triggered when user enters command "/cancel"
@router.message(Command(commands='cancel'), or_f(StateFilter(FSMCard.name_set),
                StateFilter(FSMCard.front), StateFilter(FSMCard.back)))
async def process_cancel_command(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(LEXICON[message.text], reply_markup=sets_cards_kb)

# Creating inline kb to choose a set to add card
@router.message(F.text == LEXICON['button_add_card'], StateFilter(default_state))
async def process_choose_set(message: Message, state: FSMContext):
    sets: list[str] = users_db[message.from_user.id].keys()

    if not sets:
        await message.answer(text=LEXICON['no_sets'])
    else:
        await message.answer(text=LEXICON['choose_set'],
                         reply_markup=create_listed_inline_kb(expansion=SetAddCBF,
                                                              editing=False,
                                                              args=sets)
                    )



# Saves the front side of the card into the fsm
@router.callback_query(SetAddCBF.filter(), StateFilter(default_state))
async def process_frontside(callback: CallbackQuery, state: FSMContext, callback_data: SetAddCBF):

    await state.update_data(name_set=callback_data)
    await callback.message.edit_text(text=LEXICON['front_side'])

    await state.set_state(FSMCard.front)



# Saves the back side of the card into the fsm
@router.message(StateFilter(FSMCard.front), F.text)
async def process_backside(message: Message, state: FSMContext):
    await message.answer(text=LEXICON['back_side'])
    await state.update_data(front=message.text)

    await state.set_state(FSMCard.back)


# Gets data from fsm and creates a new card in the set, clears state afterwards
@router.message(StateFilter(FSMCard.back), F.text)
async def process_set_card(message: Message, state: FSMContext):
    await state.update_data(back=message.text)

    current_state = await state.get_data()
    if current_state is None:
        return

    curr_set: str = current_state['name_set'].pack().split(':')[-1]

    users_db[message.from_user.id][curr_set][current_state['front']] = current_state['back']

    await state.clear()
    await message.answer(text=f'Отлично! Карточка {current_state['front']} = '
                         f'{current_state["back"]} была успешно создана!',
                         reply_markup=sets_cards_kb
                        )



# This is triggered when user send not text into fsm
@router.message(StateFilter(FSMCard.front), StateFilter(FSMCard.back))
async def warning_invalid_backside(message: Message):
    await message.answer(
        text=LEXICON['invalid_name']
    )