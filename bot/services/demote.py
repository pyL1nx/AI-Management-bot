async def demote_user(message, bot, user_id: int):
    await bot.promote_chat_member(
        message.chat.id,
        user_id,
        can_manage_chat=False,
        can_delete_messages=False,
        can_manage_video_chats=False,
        can_restrict_members=False,
        can_promote_members=False,
        can_change_info=False,
        can_invite_users=False,
        can_pin_messages=False,
        can_manage_topics=False,
    )
    await message.reply(f"Demoted user ID {user_id}.")
