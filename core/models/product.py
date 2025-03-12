from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer
from typing import TYPE_CHECKING

from .base import Base
from .order_product_association import order_product_association_table


if TYPE_CHECKING:
    from .order import Order


class Product(Base):
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    price: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    orders: Mapped[list["Order"]] = relationship(
        secondary=order_product_association_table,
        back_populates="products",
    )

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', price={self.price}, description='{self.description}')>"
