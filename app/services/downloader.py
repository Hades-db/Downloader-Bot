import os
import time
import hashlib
import yt_dlp
from aiogram.types import FSInputFile
from app.database.db_manager import get_cached_media, update_file_id_in_cache

def generate_url_id(url: str) -> str:
    return hashlib.md5(url.encode()).hexdigest()

async def download_and_send_media(bot, chat_id: int, url_id: str, media_type: str):
    cached = await get_cached_media(url_id, media_type)
    
    if not cached:
        await bot.send_message(chat_id, "❌ Error: Session expired. Please send the link again.")
        return

    if cached.tg_file_id:
        try:
            if media_type == "video":
                await bot.send_video(chat_id, cached.tg_file_id)
            elif media_type == "audio":
                await bot.send_audio(chat_id, cached.tg_file_id)
            elif media_type == "photo":
                await bot.send_photo(chat_id, cached.tg_file_id)
            return
        except Exception:
            pass

    if media_type == "photo":
        ydl_opts = {
            "skip_download": True,
            "quiet": True,
            "no_warnings": True
        }
    else:
        ext = "mp4" if media_type == "video" else "m4a"
        ydl_opts = {
            "format": "best[ext=mp4]/best" if media_type == "video" else "bestaudio[ext=m4a]/best",
            "outtmpl": f"downloads/%(title)s.{ext}",
            "quiet": True,
            "no_warnings": True
        }
    
    try:
        start_time = time.time()

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(cached.raw_url, download=(media_type != "photo"))
            
            if media_type == "photo":
                photo_url = info.get("thumbnail")
                if not photo_url and info.get("thumbnails"):
                    photo_url = info.get("thumbnails")[-1].get("url")
                
                if not photo_url:
                    raise ValueError("Could not extract image from this link.")
                
                elapsed_time = time.time() - start_time
                msg = await bot.send_photo(chat_id, photo_url, caption=f"Done! Extraction time: {elapsed_time:.2f} seconds.")
                if msg.photo:
                    await update_file_id_in_cache(url_id, media_type, msg.photo[-1].file_id)
                return
            else:
                filename = ydl.prepare_filename(info)

        elapsed_time = time.time() - start_time
        media_file = FSInputFile(filename)
        
        if media_type == "video":
            try:
                msg = await bot.send_video(chat_id, media_file, caption=f"Done! Loading time: {elapsed_time:.2f} seconds.")
                if msg.video:
                    await update_file_id_id_in_cache = await update_file_id_in_cache(url_id, media_type, msg.video.file_id)
            except Exception:
                msg = await bot.send_document(chat_id, media_file, caption=f"Done (Sent as document due to player codecs)! Time: {elapsed_time:.2f}s.")
                if msg.document:
                    await update_file_id_in_cache(url_id, media_type, msg.document.file_id)
                    
        elif media_type == "audio":
            msg = await bot.send_audio(chat_id, media_file, caption=f"Done! Loading time: {elapsed_time:.2f} seconds.")
            if msg.audio:
                await update_file_id_in_cache(url_id, media_type, msg.audio.file_id)

        if os.path.exists(filename):
            os.remove(filename)
            
    except Exception as e:
        await bot.send_message(chat_id, f"Error: Platform not supported or broken link. Details: {e}")
