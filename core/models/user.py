from typing import TYPE_CHECKING

from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String


if TYPE_CHECKING:
    from .post import Post
    from .profile import Profile


class User(Base):
    _user_back_populates = "user"

    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    posts: Mapped[list["Post"]] = relationship(back_populates=_user_back_populates)
    profile: Mapped["Profile"] = relationship(back_populates=_user_back_populates)
