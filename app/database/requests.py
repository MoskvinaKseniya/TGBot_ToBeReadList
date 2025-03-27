import random
from app.database.model import async_session
from app.database.model import Article, User
from sqlalchemy import select, delete, and_


# функция добавляет пользователей в бд
async def add_user(tg_id: int):
    # начинаем сессию через контекстный менеджер
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        # добавляем пользователя в бд, если он раньше не пользовался ботом
        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()


# функция сохраняет статью
async def add_article(tg_id: int, url: str):
    # начинаем сессию через контекстный менеджер
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        article = await session.scalar(select(Article).where(and_(Article.user_id == user.id, Article.url == url)))

        if not article:
            message = "Сохранил, спасибо!"
            session.add(Article(url=url, user_id=user.id))
            await session.commit()
        else:
            message = "Упс, вы уже это сохраняли :)"
        return message


# функция достает статью пользователю и удаляет её
async def get_article(tg_id: int):
    # начинаем сессию через контекстный менеджер
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        articles = await session.scalar(select(Article).where(Article.user_id == user.id))

        # выбираем случайную статью для пользователя и удаляем её из бд
        article = random.choice(articles)
        await session.execute(delete(Article).where(Article.id == article.id))
        await session.commit()
        return article
