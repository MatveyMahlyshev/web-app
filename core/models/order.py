from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, func
from datetime import datetime
from typing import TYPE_CHECKING

from .base import Base


if TYPE_CHECKING:
    from .product import Product
    from .order_product_association import OrderProductAssociation


class Order(Base):
    promocode: Mapped[str] = mapped_column(
        String(5),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=datetime.utcnow,
    )
    # products: Mapped[list["Product"]] = relationship(
    #     secondary="order_product_association",
    #     back_populates="orders",
    # )

    products_deatails: Mapped[list["OrderProductAssociation"]] = relationship(
        back_populates="order",
    )

    def __repr__(self):
        return f"<Order(id={self.id}, created at='{self.created_at}')>"
