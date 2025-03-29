import re

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

import app.database.requests as rq

# регулярное выражение для проверки ссылок
URL_PATTERN = r'^(https?|ftp):\/\/[^\s/$.?#].[^\s]*$'

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.add_user(message.from_user.id)
    await message.answer("Привет! Я бот, который поможет тебе не забыть прочитать статьи, найденные в интернете.\n"
                         "- Чтобы я запомнил статью, отправь мне ссылку на нее. Например: https://example.com\n"
                         "- Чтобы получить случайную статью из списка - отправь команду /get_article.\n"
                         "Осторожно! Отдавая статью тебе на прочтение, я удаляю её из общего списка."
                         " Тебе точно надо будет её изучить.")


# для вывода случайной записи из БД
@router.message(Command("get_article"))
async def get_link(message: Message):
    link = await rq.get_article(message.from_user.id)
    if not link:
        await message.answer("Вы пока не сохранили ни одной статьи. Если нашли что-то стоящее, я жду!")
    else:
        await message.answer("Вы хотели почитать:\n" + link + "\nСамое время это сделать!")


# для сообщений, содержащих ссылку
@router.message(lambda message: message.text and re.search(URL_PATTERN, message.text))
async def save_link(message: Message):
    # Получаем ссылку из сообщения
    url = re.search(URL_PATTERN, message.text).group(0)
    if len(url) > 256:
        await message.answer("Пожалуйста, введите ссылку размером до 256 символов.")
    else:
        await message.answer(await rq.add_article(message.from_user.id, url))


# обработка всех остальных сообщений
@router.message()
async def other_messages(message: Message):
    # if message.voice or message.video or message.photo or message.sticker or message.document or message.animation:
    if not message.text:
        await message.answer("Не понимаю вас, попробуйте отправить ссылку или одну из команд в меню.")
    else:
        await message.answer("Проверьте корректность ссылки или используйте одну из команд в меню.")
