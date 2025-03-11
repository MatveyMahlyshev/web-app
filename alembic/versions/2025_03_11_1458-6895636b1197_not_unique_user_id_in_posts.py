"""not unique user.id in posts

Revision ID: 6895636b1197
Revises: 5d08a6590df3
Create Date: 2025-03-11 14:58:58.305252

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6895636b1197"
down_revision: Union[str, None] = "5d08a6590df3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table("posts") as batch_op:
        batch_op.drop_constraint("uq_posts_user_id", type_="unique")


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("posts") as batch_op:
        batch_op.create_unique_constraint("uq_posts_user_id", ["user_id"])
