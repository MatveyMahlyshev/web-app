from pydantic import EmailStr, BaseModel, ConfigDict
from typing import Annotated
from annotated_types import MinLen, MaxLen


class UserBase(BaseModel):
    username: Annotated[str, MinLen(3), MaxLen(20)]


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class CreateUser(UserBase):
    pass

