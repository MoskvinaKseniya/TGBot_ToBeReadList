import asyncio
import logging

from aiogram import Bot, Dispatcher

from app.handlers import router
from config import TOKEN

# инициализируем подключение к тг-боту и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)


async def main():
    dp.include_router(router)
    # запрос на сервера telegram
    await dp.start_polling(bot)


# точка входа
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')
