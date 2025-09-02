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
            u = message.reply_to_message.from_user
            return u.id, u
        return None, None
    if username.startswith("@"):
        if message.reply_to_message and message.reply_to_message.from_user and \
           message.reply_to_message.from_user.username and \
           ("@" + message.reply_to_message.from_user.username.lower()) == username.lower():
            u = message.reply_to_message.from_user
            return u.id, u
    return None, None

@router.message(Command("ai"))
@admin_only()
async def ai_cmd(message: Message):
    # Grab free text after /ai
    parts = (message.text or "").split(maxsplit=1)
    task_text = parts[11] if len(parts) > 1 else ""

    # 1) Call planner
    plan = await plan_action(task_text)

    # 2) Read plan
    action = (plan.get("action") or "unknown").lower()
    username = plan.get("username")
    duration = plan.get("duration_minutes")
    reason = plan.get("reason")

    # 3) Resolve target
    uid, user = await resolve_user_id(message, username)

    # 4) Execute
    if action == "greet":
        target = user or (message.reply_to_message.from_user if message.reply_to_message else None)
        if not target:
            # Avoid HTML parse mode when echoing free text
            return await message.reply("Reply to a user to greet or include @username.", parse_mode=None)
        return await greet_user(message, target)

    if action in {"ban", "unban", "mute", "unmute", "promote", "demote"} and not uid:
        return await message.reply("User not resolved. Reply to the user's message or include @username.", parse_mode=None)

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
        # Optional guard: check that bot can actually promote to avoid silent failures
        me = await message.bot.get_chat_member(message.chat.id, (await message.bot.me()).id)
        # If the API object exposes rights, you could inspect can_promote_members here;
        # otherwise rely on Telegram to error if insufficient.
        return await promote_user(message, message.bot, uid)

    if action == "demote":
        return await demote_user(message, message.bot, uid)

    if action == "help":
        return await message.reply("Supported: greet, ban, unban, mute, unmute, promote, demote.", parse_mode=None)

    return await message.reply("Couldn't understand the task.", parse_mode=None)
