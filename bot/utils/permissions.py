from aiogram.types import ChatMemberAdministrator, ChatMemberOwner

async def is_admin(chat, user_id: int, bot) -> bool:
    member = await bot.get_chat_member(chat.id, user_id)
    return isinstance(member, (ChatMemberAdministrator, ChatMemberOwner))
