from aiogram import types
from datetime import timedelta, datetime

async def mute_user(message: types.Message, bot, user_id: int, minutes: int = 10):
    # total mute
    permissions = types.ChatPermissions(can_send_messages=False)
    until = datetime.utcnow() + timedelta(minutes=minutes)
    await bot.restrict_chat_member(
        message.chat.id,
        user_id,
        permissions=permissions,
        until_date=until
    )
    await message.reply(f"Muted user ID {user_id} for {minutes} minutes.")
