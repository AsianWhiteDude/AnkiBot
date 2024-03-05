from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from lexicon.lexicon_ru import LEXICON


# ------- Создаем клавиатуру через ReplyKeyboardBuilder -------

button_add_set = KeyboardButton(text=LEXICON['button_add_set'])
button_sets = KeyboardButton(text=LEXICON['button_sets'])
button_add_card = KeyboardButton(text=LEXICON["button_add_card"])
# Инициализируем билдер для клавиатуры с кнопками
set_card_kb_builder = ReplyKeyboardBuilder()

# Добавляем кнопки в билдер с аргументом width=1
set_card_kb_builder.row(button_sets, button_add_set, button_add_card, width=1)

# Создаем клавиатуру с кнопками
sets_cards_kb: ReplyKeyboardMarkup = set_card_kb_builder.as_markup(
    resize_keyboard=True
)
