from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from ..utils.decorators import admin_only
from ..utils.parser import parse_duration_minutes
from ..utils.ai_client import plan_action
from ..services.greet import greet_user
from ..services.ban import ban_user
from ..services.unban import unban_user
from ..services.mute import mute_user
from ..services.unmute import unmute_user
from ..services.promote import promote_user
from ..services.demote import demote_user

router = Router()
router.message.filter(F.chat.type.in_({"group", "supergroup"}))

async def resolve_user_id(message: Message, username: str | None):
    if not username:
        if message.reply_to_message and message.reply_to_message.from_user:
            return message.reply_to_message.from_user.id, message.reply_to_message.from_user
        return None, None
    if username.startswith("@"):
        # try to find via chat members if available (best-effort); fallback to mention reply
        # Telegram API doesn't provide direct username->id lookup here; users should reply to a message
        if message.reply_to_message and message.reply_to_message.from_user.username and \
           ("@" + message.reply_to_message.from_user.username.lower()) == username.lower():
            u = message.reply_to_message.from_user
            return u.id, u
    return None, None

@router.message(Command("ai"))
@admin_only()
async def ai_cmd(message: Message):
    task = (message.text or "").split(maxsplit=1)
    task_text = task[11] if len(task) > 1 else ""
    plan = await plan_action(task_text)
    action = (plan.get("action") or "unknown").lower()
    username = plan.get("username")
    duration = plan.get("duration_minutes")
    reason = plan.get("reason")

    uid, user = await resolve_user_id(message, username)
    if not uid and action not in {"help"} and action not in {"greet"}:
        return await message.reply("User not resolved. Reply to the target's message or include @username.")

    if action == "greet":
        target = user or (message.reply_to_message.from_user if message.reply_to_message else None)
        if not target:
            return await message.reply("Reply to a user to greet or specify @username in your request.")
        return await greet_user(message, target)
    if action == "ban":
        return await ban_user(message, message.bot, uid, reason)
    if action == "unban":
        return await unban_user(message, message.bot, uid)
    if action == "mute":
        mins = duration if isinstance(duration, int) else parse_duration_minutes(reason or "", 10)
        return await mute_user(message, message.bot, uid, mins)
    if action == "unmute":
        return await unmute_user(message, message.bot, uid)
    if action == "promote":
        return await promote_user(message, message.bot, uid)
    if action == "demote":
        return await demote_user(message, message.bot, uid)
    if action == "help":
        return await message.reply("Supported actions: greet, ban, unban, mute, unmute, promote, demote.")
    return await message.reply("Couldn't understand the task.")
