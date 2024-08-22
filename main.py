from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from cfg import BOT_TOKEN
from bot.handlers import start, help, db, donate, media
from data.database import initialize_db
from aiogram.contrib.middlewares.logging import LoggingMiddleware

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


dp.register_message_handler(start, commands=['start'])
dp.register_message_handler(help, commands=['help'])
dp.register_message_handler(donate, commands=['donate'])
dp.register_message_handler(db, commands=['db'])
dp.register_message_handler(media, content_types=[types.ContentType.STICKER, types.ContentType.ANIMATION, types.ContentType.ANY])

if __name__ == '__main__':
    initialize_db()
    # register_handlers(dp)
    executor.start_polling(dp, skip_updates=True)
