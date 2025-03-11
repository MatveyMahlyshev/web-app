import asyncio
from core.models import db_helper, User, Profile, Post
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result
from sqlalchemy.orm import joinedload


async def create_user(session: AsyncSession, username: str) -> User:
    user = User(username=username)
    session.add(user)
    await session.commit()
    return user


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    user: User | None = await session.scalar(statement=stmt)
    if user:
        print("found user", username, user)
    return user


async def create_profile(
    session: AsyncSession,
    user_id: int,
    first_name: str | None = None,
    last_name: str | None = None,
) -> Profile:

    profile = Profile(
        user_id=user_id,
        first_name=first_name,
        last_name=last_name,
    )
    session.add(profile)
    await session.commit()
    return profile


async def show_users_with_profiles(session: AsyncSession) -> list[User]:
    stmt = select(User).options(joinedload(User.profile)).order_by(User.id)
    users = await session.scalars(statement=stmt)
    for user in users:
        print(user)
        print(user.profile.first_name)


async def create_post(
    session: AsyncSession, user_id: int, *post_titles: str
) -> list[Post]:

    posts = [Post(title=title, user_id=user_id) for title in post_titles]
    session.add_all(posts)
    await session.commit()
    return posts


async def main():
    async with db_helper.session_factory() as session:
        user = await get_user_by_username(session=session, username="Artem")

        await create_post(
            session,
            user.id,
            "fastapi",
            "django",
            "alembic",
        )


if __name__ == "__main__":
    asyncio.run(main())
