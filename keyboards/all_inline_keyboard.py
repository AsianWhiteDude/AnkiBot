from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from lexicon.lexicon_ru import LEXICON



def create_listed_inline_kb(expansion: CallbackData,
                            callback_args: dict[str, str] = {},
                           args: list[str] = [],
                           kwargs: dict[str, str] = {},
                           editing: bool = True,
                           special_smbl: str = '',
                           ) -> InlineKeyboardMarkup:
    #Creates inline kb with list of buttons



    # Creating inline kb builder
    kb_builder = InlineKeyboardBuilder()

    #Adding all buttons in a list of args ordered by arg asc
    for button in sorted(args):
        kb_builder.row(InlineKeyboardButton(
            text=f'{special_smbl + button}',
            callback_data=expansion(set_name=button, *callback_args).pack()
        ))

    #Adding all buttons in a dict of kwargs orders by key asc
    for key_value in sorted(kwargs.items(), key=lambda x: x[0]):
        key, value = key_value
        kb_builder.row(InlineKeyboardButton(
            text=f'{special_smbl}{key}: {value}',
            callback_data=expansion(set_name=key, *callback_args).pack()
        ))


    # Adding buttons for 'editing' and 'canceling' or just 'canceling'
    if editing:
        kb_builder.row(
            InlineKeyboardButton(
                text=LEXICON['edit_sets'],
                callback_data='edit_sets'
            ),
            InlineKeyboardButton(
                text=LEXICON['cancel'],
                callback_data='cancel'
            ),
            width=2
        )
    else:
        kb_builder.row(
            InlineKeyboardButton(
                text=LEXICON['cancel'],
                callback_data='cancel'
            ),
            width=1
        )

    return kb_builder.as_markup()
