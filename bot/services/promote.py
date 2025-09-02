async def promote_user(message, bot, user_id: int):
    # Minimal example: can_manage_chat True; refine as needed
    await bot.promote_chat_member(
        message.chat.id,
        user_id,
        can_manage_chat=True,
        can_delete_messages=True,
        can_manage_video_chats=True,
        can_restrict_members=True,
        can_promote_members=False,
        can_change_info=False,
        can_invite_users=True,
        can_pin_messages=True,
        can_manage_topics=True,
    )
    await message.reply(f"Promoted user ID {user_id}.")
