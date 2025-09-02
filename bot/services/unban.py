from aiogram import types

async def unban_user(message: types.Message, bot, user_id: int):
    await bot.unban_chat_member(message.chat.id, user_id, only_if_banned=True)
    await message.reply(f"Unbanned user ID {user_id}.")
