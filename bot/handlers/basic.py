from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from ..utils.constants import HELP_TEXT

router = Router()
router.message.filter(F.chat.type.in_({"private", "group", "supergroup"}))

@router.message(Command("start"))
async def start_cmd(message: Message):
    await message.reply("Hello! I'm a management bot. Use /help to see commands.")

@router.message(Command("help"))
async def help_cmd(message: Message):
    await message.reply(HELP_TEXT)

@router.message(Command("ping"))
async def ping_cmd(message: Message):
    await message.reply("pong")
