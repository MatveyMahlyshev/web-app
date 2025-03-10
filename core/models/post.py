from .base import Base
from .mixins import UserRelationMixin
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text


class Post(UserRelationMixin, Base):

    _user_back_populates = "posts"
    _user_id_unique = True

    title: Mapped[str] = mapped_column(String(100), nullable=False)
    body: Mapped[str] = mapped_column(
        Text,
        default="",
        server_default="",
    )
