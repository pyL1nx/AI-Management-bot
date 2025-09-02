from aiogram import types

async def ban_user(message: types.Message, bot, user_id: int, reason: str | None = None):
    await bot.ban_chat_member(message.chat.id, user_id)
    text = f"Banned user ID {user_id}."
    if reason:
        text += f" Reason: {reason}"
    await message.reply(text)
