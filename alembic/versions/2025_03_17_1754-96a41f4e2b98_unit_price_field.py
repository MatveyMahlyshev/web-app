"""unit_price field

Revision ID: 96a41f4e2b98
Revises: f6fa0b616a2d
Create Date: 2025-03-17 17:54:19.393607

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "96a41f4e2b98"
down_revision: Union[str, None] = "f6fa0b616a2d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Добавляем новый столбец без server_default
    op.add_column(
        "order_product_association",
        sa.Column("unit_price", sa.Integer(), nullable=True),
    )

    # Обновляем все существующие записи, устанавливая unit_price = 0
    op.execute("UPDATE order_product_association SET unit_price = 0")

    # Делаем столбец NOT NULL после обновления
    with op.batch_alter_table("order_product_association") as batch_op:
        batch_op.alter_column("unit_price", nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("order_product_association", "unit_price")
