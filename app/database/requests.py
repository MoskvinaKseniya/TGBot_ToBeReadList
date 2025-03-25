from app.database.model import async_session
from app.database.model import Article, User
from sqlalchemy import select


async def set_user(tg_id):
    # начинаем сессию через контекстный менеджер
    async with async_session() as session:
        # проверка, существует ли пользователь в бд
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        # добавляем пользователя в бд, если он раньше не пользовался ботом
        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()
