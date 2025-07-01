import os
import asyncio
import logging
from aiogram import Bot, Dispatcher
from handlers import start, quiz
from services.db import create_table

# Берём токен из переменных окружения
API_TOKEN = os.getenv("API_TOKEN")

# Включаем логгирование
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Регистрируем хендлеры
start.register_handlers(dp)
quiz.register_handlers(dp)

async def main():
    await create_table()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
