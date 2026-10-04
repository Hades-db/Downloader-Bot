import asyncio
import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from app.handlers import commands, media, callback
from app.database.db_manager import init_db

async def main():
    load_dotenv()
    
    token = os.getenv("TOKEN")
    if not token:
        print("[Error] TOKEN variable is missing inside .env file!")
        return

    bot = Bot(token=token)
    dp = Dispatcher()
    
    try:
        await init_db()
        
        if not os.path.exists("downloads"):
            os.makedirs("downloads")
            
        dp.include_router(commands.router)
        dp.include_router(media.router)
        dp.include_router(callback.router)
        
        print("Bot Start")
        await dp.start_polling(bot)
        
    except Exception as ex:
        print(f"There is an Exception: {ex}")
    finally:
        await bot.session.close()
        print("Bot Off!")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nBot Off manually.")