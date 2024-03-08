from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon_ru import LEXICON



def choice_of_sets_or_cards_kb() -> InlineKeyboardMarkup:
    #kb for choosing between sets and cards


    #Initializing kb builder
    kb_builder = InlineKeyboardBuilder()

    #Adding buttons into kb builder with width=2
    kb_builder.row(
            InlineKeyboardButton(
                text=LEXICON['button_sets'],
                callback_data='button_sets'
            ),
            InlineKeyboardButton(
                text=LEXICON['button_cards'],
                callback_data='button_cards'
            ),
            width=2
    )

    return kb_builder.as_markup()



def study_kb(side: str) -> InlineKeyboardMarkup:
    #kb for choosing between sets and cards


    #Initializing kb builder
    kb_builder = InlineKeyboardBuilder()

    #Adding buttons into kb builder with width=2
    kb_builder.row(
            InlineKeyboardButton(
                text=LEXICON['answer'],
                callback_data=side
            ),
            InlineKeyboardButton(
                text=LEXICON['hint'],
                callback_data='hint'
            ),
            InlineKeyboardButton(
                text=LEXICON['next'],
                callback_data='next'
            ),
            width=3
    )

    return kb_builder.as_markup()