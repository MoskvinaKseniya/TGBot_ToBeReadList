import re
import app.database.requests as rq
from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

# Регулярное выражение для проверки ссылок
URL_PATTERN = r'(https?://[^\s]+)'

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer("Привет! Я бот, который поможет тебе не забыть прочитать статьи, найденные в интернете.\n"
                         "- Чтобы я запомнил статью, отправь мне ссылку на нее. Например: https://example.com\n"
                         "- Чтобы получить случайную статью из списка - отправь команду /get_article.\n"
                         "Осторожно! Отдавая статью тебе на прочтение, я удаляю её из общего списка."
                         " Тебе точно надо будет её изучить.")


# Для вывода случайной записи из БД
@router.message(Command("get_article"))
async def get_link(message: Message):
    link = 'https://example.com'
    if link != '':
        await message.answer("Вы хотели почитать:\n" + link + "\nСамое время это сделать!")
    else:
        await message.answer("Вы пока не сохранили ни одной статьи :( Если нашли что-то стоящее, я жду!")


# Для сообщений, содержащих ссылку
@router.message(lambda message: re.search(URL_PATTERN, message.text))
async def save_link(message: Message):
    # Получаем ссылку из сообщения
    url = re.search(URL_PATTERN, message.text).group(0)

    # Здесь можно добавить любую логику для работы с полученной ссылкой
    if True:
        await message.reply("Сохранил, спасибо!")
    else:
        await message.reply("Упс, вы уже это сохраняли :)")
