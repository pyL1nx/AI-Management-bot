from aiogram import BaseMiddleware
from aiogram.types import Message
from ..utils.permissions import is_admin

class AdminGateMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data):
        txt = event.text or ""
        admin_cmds = ("/ban", "/unban", "/mute", "/unmute", "/promote", "/demote", "/ai", "/greet")
        if txt.startswith(admin_cmds):
            if not await is_admin(event.chat, event.from_user.id, event.bot):
                await event.reply("Only admins can run this.")
                return
        return await handler(event, data)
