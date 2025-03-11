from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession


from users import crud
from core.models import db_helper
from .schemas import User, CreateUser


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[User])
async def get_users(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_all_users(session=session)


@router.post("/", response_model=CreateUser, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: CreateUser,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_user(session=session, user_in=user_in)


@router.get("/{user_id}", response_model=User)
async def get_user_by_id(session: AsyncSession = Depends(db_helper.scoped_session_dependency), user_id: int = 1):
    return await crud.get_user_by_id(session=session, user_id=user_id)

