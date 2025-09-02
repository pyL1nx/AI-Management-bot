from aiogram import types

async def unmute_user(message: types.Message, bot, user_id: int):
    # restore default send permission
    permissions = types.ChatPermissions(can_send_messages=True)
    await bot.restrict_chat_member(
        message.chat.id,
        user_id,
        permissions=permissions
    )
    await message.reply(f"Unmuted user ID {user_id}.")
