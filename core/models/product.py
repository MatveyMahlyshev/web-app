from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer
from typing import TYPE_CHECKING

from .base import Base


if TYPE_CHECKING:
    from .order_product_association import OrderProductAssociation


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
    # orders: Mapped[list["Order"]] = relationship(
    #     secondary="order_product_association",
    #     back_populates="products",
    # )

    orders_details: Mapped[list["OrderProductAssociation"]] = relationship(
        back_populates="product",
    )

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', price={self.price}, description='{self.description}')>"
