from aiogram import F, Router
from aiogram.filters import  StateFilter
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, CallbackQuery
from database.database import users_db
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, StatesGroup
from keyboards.all_inline_keyboard import create_listed_inline_kb
from keyboards.other_keyboards import study_kb
from lexicon.lexicon_ru import LEXICON
from random import randint
from services.services import get_hint

router = Router()

# Creating state machine to keep track of cards in the set
class FSMCards(StatesGroup):

    prev_card: int
    cards = dict[str, str]


# CBF - Callback Factory. Makes it easier to get data from
# Callbacks when you have changing data
class StudySetCBF(CallbackData, prefix='study_set'):
    set_name: str



@router.message(F.text == LEXICON['button_study'])
async def process_choose_set(message: Message):
    sets: list[str] = users_db[message.from_user.id].keys()

    if not sets:
        await message.answer(text=LEXICON['no_sets'])
    else:
        await message.answer(text=LEXICON['choose_set'],
                            reply_markup=create_listed_inline_kb(expansion=StudySetCBF,
                                                                editing=False,
                                                                args=sets)
                        )



@router.callback_query(StudySetCBF.filter(), StateFilter(default_state))
async def study_set_button(callback: CallbackQuery,
                              callback_data: StudySetCBF,
                              state: FSMContext):
    key_set = callback_data.pack().split(':')[1]
    cards = users_db[callback.from_user.id][key_set]
    if not cards:
        text = f'{key_set}: ' + LEXICON['no_cards']
        await callback.message.edit_text(
                text=text
            )
    else:
        await state.update_data(cards=cards)
        await state.update_data(prev_card=0)

        current_state = await state.get_data()
        cards = current_state['cards']
        curr_card = randint(0, len(cards)-1)

        await callback.message.edit_text(text=list(cards)[curr_card], reply_markup=study_kb('front'))
        await state.update_data(prev_card=curr_card)

@router.callback_query(F.data == 'next')
async def next_button(callback: CallbackQuery,
                              state: FSMContext,
                              ):
    current_state = await state.get_data()
    cards = current_state['cards']
    prev_card = current_state['prev_card']

    if len(cards) == 1:
        await callback.answer()
        return

    curr_card = randint(0, len(cards)-1)
    while prev_card == curr_card:
        curr_card = randint(0, len(cards)-1)

    await callback.message.edit_text(text=list(cards)[curr_card], reply_markup=study_kb('front'))
    await state.update_data(prev_card=curr_card)

@router.callback_query(F.data == 'front')
async def to_front_button(callback: CallbackQuery,
                              state: FSMContext,
                              ):
    current_state = await state.get_data()
    cards = current_state['cards']
    prev_card = current_state['prev_card']

    back = cards[list(cards)[prev_card]]

    await callback.message.edit_text(text=back, reply_markup=study_kb('back'))

@router.callback_query(F.data == 'back')
async def to_back_button(callback: CallbackQuery,
                              state: FSMContext,
                              ):
    current_state = await state.get_data()
    cards = current_state['cards']
    prev_card = current_state['prev_card']

    front = list(cards)[prev_card]

    await callback.message.edit_text(text=front, reply_markup=study_kb('front'))


@router.callback_query(F.data == 'hint')
async def hint_button(callback: CallbackQuery,
                              state: FSMContext,
                              ):
    current_state = await state.get_data()
    cards = current_state['cards']
    prev_card = current_state['prev_card']

    front = list(cards)[prev_card]
    hint = get_hint(cards[front])
    text = front + '\n\nПодсказка: ' + hint
    if text == callback.message.text:
        await callback.answer()
    else:
        await callback.message.edit_text(text=text,
                                     reply_markup=callback.message.reply_markup)
