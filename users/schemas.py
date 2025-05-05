from pydantic import EmailStr, BaseModel, ConfigDict
from typing import Annotated
from annotated_types import MinLen, MaxLen


class UserBase(BaseModel):
    username: Annotated[str, MinLen(3), MaxLen(20)]


class UserSchema(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class CreateUser(UserBase):
    pass


class UserAuthSchema(BaseModel):
    model_config = ConfigDict(strict=True)
    username: str
    password: bytes
    email: EmailStr | None = None
    active: bool = True
