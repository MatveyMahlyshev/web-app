from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result
from sqlalchemy.orm import joinedload, selectinload
import asyncio

from core.models import User, Profile, Post, db_helper
from users.schemas import CreateUser
from core.models import Product, Order


async def create_user(session: AsyncSession, user_in: CreateUser) -> User | None:
    user = User(**user_in.model_dump())
    session.add(user)
    await session.commit()
    return user


async def get_all_users(session: AsyncSession) -> list[User]:
    stmt = select(User).order_by(User.id)
    result: Result = await session.execute(statement=stmt)
    users = result.scalars().all()
    return list(users)


async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    return await session.get(User, user_id)


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
    return users


async def create_post(
    session: AsyncSession, user_id: int, *post_titles: str
) -> list[Post]:

    posts = [Post(title=title, user_id=user_id) for title in post_titles]
    session.add_all(posts)
    await session.commit()
    return posts


async def get_users_with_posts(session: AsyncSession):
    stmt = select(User).options(selectinload(User.posts)).order_by(User.id)
    users = await session.scalars(statement=stmt)
    for user in users:
        print("**" * 10)
        print(user)
        for post in user.posts:
            print("-", post)


async def get_users_with_posts_and_profile(session: AsyncSession):
    stmt = (
        select(User)
        .options(joinedload(User.profile), selectinload(User.posts))
        .order_by(User.id)
    )
    users = await session.scalars(statement=stmt)
    for user in users:
        print("**" * 10)
        print(user, user.profile and user.profile.last_name)
        for post in user.posts:
            print("-", post)


async def get_profiles_with_users_and_users_with_posts(session: AsyncSession):
    stmt = (
        select(Profile)
        .join(Profile.user)
        .options(joinedload(Profile.user).selectinload(User.posts))
        .order_by(Profile.id)
        .where(User.username == "Artem")
    )
    profiles = await session.scalars(statement=stmt)
    for profile in profiles:
        print(profile.first_name, profile.user)
        print(profile.user.posts)


async def get_posts_with_authors(session: AsyncSession, user_id: int) -> list[Post]:
    stmt = (
        select(Post)
        .options(selectinload(Post.user))
        .where(Post.user_id == user_id)
        .order_by(Post.title)
    )
    posts = list(await session.scalars(statement=stmt))
    return posts


async def create_order(
    session: AsyncSession,
    promocode: str | None = None,
) -> Order:
    order = Order(promocode=promocode)
    session.add(order)
    await session.commit()
    return order


async def create_product(
    session: AsyncSession,
    name: str,
    description: str,
    price: int,
) -> Product:
    product = Product(name=name, description=description, price=price)
    session.add(product)
    await session.commit()
    return product


async def get_orders_with_products(session: AsyncSession) -> list[Order]:
    stmt = select(Order).options(
        selectinload(Order.products),
    ).order_by(Order.id)

    orders = await session.scalars(statement=stmt)
    return list(orders)



async def demo_m2m(session: AsyncSession):
    order_one = await create_order(session=session)
    order_promo = await create_order(
        session=session,
        promocode="fastapi",
    )
    mouse = await create_product(
        session=session,
        name="Bloody TL7",
        description="Great computer mouse!",
        price=20,
    )
    keyboard = await create_product(
        session=session,
        name="Redragon ELF",
        description="Good mechanic keyboard!",
        price=40,
    )
    display = await create_product(
        session=session,
        name="Samsung",
        description="Old monitor()",
        price=60,
    )
    order_one = await session.scalar(
        select(Order)
        .where(Order.id == order_one.id)
        .options(selectinload(Order.products)),
    )
    order_promo = await session.scalar(
        select(Order)
        .where(Order.id == order_promo.id)
        .options(selectinload(Order.products)),
    )
    order_one.products.append(mouse)
    order_one.products.append(keyboard)
    order_promo.products.append(keyboard)
    order_promo.products.append(display)

    await session.commit()


async def main():
    async with db_helper.session_factory() as session:
        await demo_m2m(session=session)


if __name__ == "__main__":
    asyncio.run(main=main())
