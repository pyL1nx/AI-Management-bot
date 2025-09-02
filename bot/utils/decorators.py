from aiogram import types
from aiogram.exceptions import TelegramBadRequest
from .permissions import is_admin

def admin_only():
    def wrapper(handler):
        async def inner(message: types.Message, *args, **kwargs):
            if not message.chat or message.chat.type not in {"group", "supergroup"}:
                return await message.reply("This command can be used only in group chats.")
            if not await is_admin(message.chat, message.from_user.id, message.bot):
                return await message.reply("Only admins can run this.")
            try:
                return await handler(message, *args, **kwargs)
            except TelegramBadRequest as e:
                return await message.reply(f"Telegram error: {e.message}")
        return inner
    return wrapper
