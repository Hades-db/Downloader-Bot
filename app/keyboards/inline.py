from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app import ui_text

async def get_format_keyboard(url_id: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=ui_text.KB_VIDEO, callback_data=f"video|{url_id}")],
            [InlineKeyboardButton(text=ui_text.KB_AUDIO, callback_data=f"audio|{url_id}")],
            [InlineKeyboardButton(text=ui_text.KB_PHOTO, callback_data=f"photo|{url_id}")]
        ]
    )
    return keyboard