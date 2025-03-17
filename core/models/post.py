from .base import Base
from .mixins import UserRelationMixin
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text


class Post(UserRelationMixin, Base):

    _user_back_populates = "posts"
    _user_id_unique = False

    title: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    body: Mapped[str] = mapped_column(
        Text,
        default="",
        server_default="",
    )

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, username={self.title}, user_id={self.user_id})"

    def __repr__(self):
        return str(self)
