from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from lexicon.lexicon_ru import LEXICON


# ------- Создаем клавиатуру через ReplyKeyboardBuilder -------

button_add_set = KeyboardButton(text=LEXICON['button_add_set'])
button_sets = KeyboardButton(text=LEXICON['button_sets'])
button_add_card = KeyboardButton(text=LEXICON["button_add_card"])
# Инициализируем билдер для клавиатуры с кнопками
yes_no_kb_builder = ReplyKeyboardBuilder()

# Добавляем кнопки в билдер с аргументом width=3
yes_no_kb_builder.row(button_sets, button_add_set, button_add_card, width=3)

# Создаем клавиатуру с кнопками
yes_no_kb: ReplyKeyboardMarkup = yes_no_kb_builder.as_markup(
    resize_keyboard=True
)
