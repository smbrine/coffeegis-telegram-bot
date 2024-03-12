"""added inline requests counter nullable

Revision ID: 58fb855701cf
Revises: 4af431244444
Create Date: 2024-03-12 19:17:12.812474

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "58fb855701cf"
down_revision: Union[str, None] = "4af431244444"
branch_labels: Union[str, Sequence[str], None] = (
    None
)
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "profiles",
        sa.Column(
            "inline_search_requests",
            sa.BigInteger(),
            nullable=True,
        ),
    )
    op.alter_column(
        "profiles",
        "is_phone_confirmed",
        existing_type=sa.INTEGER(),
        nullable=False,
    )
    op.alter_column(
        "users",
        "is_premium",
        existing_type=sa.BOOLEAN(),
        nullable=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "users",
        "is_premium",
        existing_type=sa.BOOLEAN(),
        nullable=True,
    )
    op.alter_column(
        "profiles",
        "is_phone_confirmed",
        existing_type=sa.INTEGER(),
        nullable=True,
    )
    op.drop_column(
        "profiles", "inline_search_requests"
    )
    # ### end Alembic commands ###