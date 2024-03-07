from aiogram import Router
from aiogram.types import Message
from lexicon.lexicon_ru import LEXICON

router = Router()

# This handler gets triggered by any user messages that are not
# supposed to be handled by this bot
@router.message()
async def send_echo_response(message: Message):
    await message.answer(LEXICON['echo_response'])
