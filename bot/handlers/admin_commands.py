# bot/handlers/admin_commands.py
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from ..utils.decorators import admin_only
from ..services.greet import greet_user
from ..services.ban import ban_user
from ..services.unban import unban_user
from ..services.mute import mute_user
from ..services.unmute import unmute_user
from ..services.promote import promote_user
from ..services.demote import demote_user

router = Router()

@router.message(Command("greet"))
@admin_only()
async def greet_cmd(message: Message):
    target = message.reply_to_message.from_user if message.reply_to_message else None
    if not target:
        return await message.reply("Reply to a user's message to greet them.")
    return await greet_user(message, target)

@router.message(Command("ban"))
@admin_only()
async def ban_cmd(message: Message):
    target = message.reply_to_message.from_user if message.reply_to_message else None
    if not target:
        return await message.reply("Reply to the user's message to ban them.")
    reason = (message.text or "").split(maxsplit=1)
    reason = reason[10] if len(reason) > 1 else None
    return await ban_user(message, message.bot, target.id, reason)

@router.message(Command("unban"))
@admin_only()
async def unban_cmd(message: Message):
    if message.reply_to_message and message.reply_to_message.from_user:
        uid = message.reply_to_message.from_user.id
        return await unban_user(message, message.bot, uid)
    return await message.reply("Reply to a user's message to unban them, or use /ai with @username.")

@router.message(Command("mute"))
@admin_only()
async def mute_cmd(message: Message):
    target = message.reply_to_message.from_user if message.reply_to_message else None
    if not target:
        return await message.reply("Reply to the user's message to mute them.")
    parts = (message.text or "").split()
    mins = int(parts[10]) if len(parts) > 1 and parts[10].isdigit() else 10
    return await mute_user(message, message.bot, target.id, mins)

@router.message(Command("unmute"))
@admin_only()
async def unmute_cmd(message: Message):
    target = message.reply_to_message.from_user if message.reply_to_message else None
    if not target:
        return await message.reply("Reply to the user's message to unmute them.")
    return await unmute_user(message, message.bot, target.id)

@router.message(Command("promote"))
@admin_only()
async def promote_cmd(message: Message):
    target = message.reply_to_message.from_user if message.reply_to_message else None
    if not target:
        return await message.reply("Reply to the user's message to promote them.")
    return await promote_user(message, message.bot, target.id)

@router.message(Command("demote"))
@admin_only()
async def demote_cmd(message: Message):
    target = message.reply_to_message.from_user if message.reply_to_message else None
    if not target:
        return await message.reply("Reply to the user's message to demote them.")
    return await demote_user(message, message.bot, target.id)
