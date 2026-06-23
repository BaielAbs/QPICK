import os
import asyncio
import django
from aiogram import Bot, Dispatcher
from had.user import router

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

TOKEN = "8811617979:AAHdX3Kfm42RY-nhp0vwKTGEYhggFDIbNcE"

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    dp.include_router(router)

    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass