from aiogram import types
from ..utils.constants import GREETING_TEXT

async def greet_user(message: types.Message, target: types.User):
    mention = target.mention_html(target.full_name)
    await message.reply(GREETING_TEXT.format(mention=mention))
