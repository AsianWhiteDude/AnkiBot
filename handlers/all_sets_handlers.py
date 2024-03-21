from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters.callback_data import CallbackData
from sqlalchemy.orm import sessionmaker
from database.db_commands import get_decks, get_cards, del_deck, del_card
from keyboards.all_inline_keyboard import create_listed_inline_kb
from keyboards.other_keyboards import choice_of_sets_or_cards_kb
from lexicon.lexicon_ru import LEXICON


router = Router()



# CBF - Callback Factory. Makes it easier to get data from
# Callbacks when you have changing data
class SetCBF(CallbackData, prefix='set'):
    set_name: str

class SetCardsCBF(CallbackData, prefix='set_cards'):
    set_name: str

class SetDelCBF(CallbackData, prefix='set_del'):
    set_name: str

class CardDelCBF(CallbackData, prefix='card_del'):
    set_name: str
    card: str

# Shows all sets in inline buttons func
@router.message(F.text == LEXICON['button_sets'])
async def process_all_sets(message: Message,
                           session_maker: sessionmaker):
    sets: list[str] = await get_decks(user_id=message.from_user.id, session_maker=session_maker)

    if not sets:
        await message.answer(text=LEXICON['no_sets'])
    else:
        await message.answer(text=LEXICON['keyboard_sets'],
                   reply_markup=create_listed_inline_kb(expansion=SetCBF,
                                                        args=sets))


# This handler is triggered when user presses any set button
# and shows all the cards inside if there are any
@router.callback_query(SetCBF.filter())
async def response_set_button(callback: CallbackQuery,
                              callback_data: SetCBF,
                              session_maker: sessionmaker):
    key_set = callback_data.pack().split(':')[1]
    cards = get_cards(user_id=callback.from_user.id, set_name=key_set, session_maker=session_maker)
    if not cards:
        text = f'{key_set}: ' + LEXICON['no_cards']
        await callback.message.edit_text(
                text=text
            )
    else:
        text = f'Все карточки из колоды:\n\n{key_set}:\n' + \
        '\n'.join([f'{key}: {value}' for key, value in cards.items()])
        await callback.message.edit_text(
                text=text
            )

# Edit button. Gives you a choice of what you want to edit cards or sets
@router.callback_query(F.data == 'edit_sets')
async def response_editing_button(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON['choose_del_set_card'],
                                     reply_markup=choice_of_sets_or_cards_kb())

# Shows all sets. On press deletes the set
@router.callback_query(F.data == 'button_sets')
async def response_edit_sets(callback: CallbackQuery, session_maker: sessionmaker):
    sets: list[str] = await get_decks(user_id=callback.from_user.id, session_maker=session_maker)
    del_sets = create_listed_inline_kb(expansion=SetDelCBF,
                                       args=sets,
                                       editing=False,
                                       special_smbl=LEXICON['del_smbl'])

    await callback.message.edit_text(text=LEXICON['del_set'],
                                     reply_markup=del_sets)

# Shows all sets. On press shows all cards of the set
@router.callback_query(F.data == 'button_cards')
async def response_edit_cards(callback: CallbackQuery, session_maker:sessionmaker):
    sets: list[str] = await get_decks(user_id=callback.from_user.id, session_maker=session_maker)
    del_sets = create_listed_inline_kb(expansion=SetCardsCBF,
                                       args=sets,
                                       editing=False)

    await callback.message.edit_text(text=LEXICON['choose_set'],
                                     reply_markup=del_sets)


# Deletes the set that was triggered
@router.callback_query(SetDelCBF.filter())
async def response_del_set(callback: CallbackQuery, callback_data: SetDelCBF,
                           session_maker: sessionmaker):
    from_set = callback_data.pack().split(':')[1]
    await del_deck(user_id=callback.from_user.id, set_name=from_set, session_maker=session_maker)
    sets: list[str] = await get_decks(user_id=callback.from_user.id, session_maker=session_maker)

    if not sets:
        await callback.message.edit_text(text=LEXICON['no_sets'])
    else:
        del_sets = create_listed_inline_kb(expansion=SetDelCBF,
                                        args=sets,
                                        editing=False,
                                        special_smbl=LEXICON['del_smbl'])

        await callback.answer(text=LEXICON['success'])
        await callback.message.edit_text(text=LEXICON['choose_del_set_card'],
                                        reply_markup=del_sets)


# Shows all cards of the set that was pressed
@router.callback_query(SetCardsCBF.filter())
async def response_choose_card_to_del(callback: CallbackQuery,
                                      callback_data: SetCardsCBF,
                                      session_maker: sessionmaker):
    from_set = callback_data.pack().split(':')[1]
    cards = get_cards(user_id=callback.from_user.id, set_name=from_set, session_maker=session_maker)

    if not cards:
        await callback.message.edit_text(text=LEXICON['no_cards'])
    else:
        chosen_set_to_del_card = create_listed_inline_kb(expansion=CardDelCBF,
                                                        set_name=from_set,
                                                        kwargs=cards,
                                                        editing=False,
                                                        special_smbl=LEXICON['del_smbl'])

        await callback.message.edit_text(text=LEXICON['del_choosen_card'],
                                        reply_markup=chosen_set_to_del_card)



# Deletes the card that was pressed
@router.callback_query(CardDelCBF.filter())
async def response_del_card(callback: CallbackQuery,
                            callback_data: CardDelCBF,
                            session_maker: sessionmaker):
    from_set, card_key = callback_data.pack().split(':')[1:]
    await del_card(user_id=callback.from_user.id, key=card_key, session_maker=session_maker)

    cards = get_cards(user_id=callback.from_user.id, set_name=from_set, session_maker=session_maker)

    if not cards:
        await callback.message.edit_text(text=LEXICON['no_cards'])
    else:
        del_sets = create_listed_inline_kb(expansion=SetDelCBF,
                                        kwargs=cards,
                                        editing=False,
                                        special_smbl=LEXICON['del_smbl'])

        await callback.answer(text=LEXICON['success'])
        await callback.message.edit_text(text=LEXICON['choose_del_set_card'],
                                        reply_markup=del_sets)




# Cancel button. Deletes attached message and last user's message
@router.callback_query(F.data == 'cancel')
async def response_cancel_button(call: CallbackQuery):
    await call.answer(text=LEXICON['/cancel'])

    try:
        await call.bot.delete_message(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id-1)
    except:
        pass

    await call.message.delete()