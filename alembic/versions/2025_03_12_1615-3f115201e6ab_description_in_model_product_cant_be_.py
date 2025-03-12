"""description in model Product cant be nullable

Revision ID: 3f115201e6ab
Revises: 0cee4ff872cc
Create Date: 2025-03-12 16:15:13.916511

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3f115201e6ab"
down_revision: Union[str, None] = "0cee4ff872cc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # SQLite requires creating a temporary table to modify nullable constraint
    with op.batch_alter_table("products") as batch_op:
        batch_op.alter_column("description", existing_type=sa.String(length=255), nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    # SQLite requires creating a temporary table to modify nullable constraint
    with op.batch_alter_table("products") as batch_op:
        batch_op.alter_column("description", existing_type=sa.String(length=255), nullable=True)