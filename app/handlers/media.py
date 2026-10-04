from aiogram import Router
from aiogram.types import Message
from app import ui_text
from app.keyboards.inline import get_format_keyboard
from app.services.downloader import generate_url_id
from app.database.db_manager import save_url_to_cache

router = Router()

@router.message(lambda message: message.text and (message.text.startswith("http://") or message.text.startswith("https://")))
async def video_request(message: Message):
    url = message.text.strip()
    url_id = generate_url_id(url)
    
    await save_url_to_cache(url_id, url, media_type="video")
    await save_url_to_cache(url_id, url, media_type="audio")
    await save_url_to_cache(url_id, url, media_type="photo")
    
    keyboard = await get_format_keyboard(url_id)
    await message.answer(ui_text.KB_TITLE, reply_markup=keyboard)