from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from lexicon.lexicon_ru import LEXICON


# ------- Creating keyboard using ReplyKeyboardBuilder -------

button_add_set = KeyboardButton(text=LEXICON['button_add_set'])
button_sets = KeyboardButton(text=LEXICON['button_sets'])
button_add_card = KeyboardButton(text=LEXICON["button_add_card"])

# Initializing keyboard builder
set_card_kb_builder = ReplyKeyboardBuilder()

# Adding buttons in kb builder with argument width=1
set_card_kb_builder.row(button_sets, button_add_set, button_add_card, width=1)

# Creating keyboard with buttons
sets_cards_kb: ReplyKeyboardMarkup = set_card_kb_builder.as_markup(
    resize_keyboard=True
)
