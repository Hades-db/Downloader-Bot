from aiogram import Bot, Router
from aiogram.types import CallbackQuery
from app.services.downloader import download_and_send_media

router = Router()

@router.callback_query(lambda callback: any(action in callback.data for action in ["video|", "audio|", "photo|"]))
async def format_selection(callback: CallbackQuery, bot: Bot):
    action, url_id = callback.data.split("|")
    await callback.answer("Confirmed!")
    
    if action == "video":
        await callback.message.answer("📥 Processing video stream... Please wait.")
        await download_and_send_media(bot, callback.message.chat.id, url_id, media_type="video")
    elif action == "audio":
        await callback.message.answer("📥 Processing audio stream... Please wait.")
        await download_and_send_media(bot, callback.message.chat.id, url_id, media_type="audio")
    elif action == "photo":
        await callback.message.answer("📥 Extracting image/photo... Please wait.")
        await download_and_send_media(bot, callback.message.chat.id, url_id, media_type="photo")