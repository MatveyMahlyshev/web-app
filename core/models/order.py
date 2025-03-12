from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, func
from datetime import datetime

from .base import Base


class Order(Base):
    promocode: Mapped[str] = mapped_column(String(5), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=datetime.utcnow
    )

    def __repr__(self):
        return (
            f"<Order(id={self.id}, created at='{self.created_at}')>"
        )
