from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from app import ui_text
from app.database.db_manager import register_user

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await register_user(message.from_user.id)
    await message.reply(ui_text.CMD_START, parse_mode="Markdown")