"""changed ids to bigint

Revision ID: c316f22d9741
Revises: 69b9b351d865
Create Date: 2024-03-12 18:32:17.921240

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c316f22d9741"
down_revision: Union[str, None] = "69b9b351d865"
branch_labels: Union[str, Sequence[str], None] = (
    None
)
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "profiles",
        "user_telegram_id",
        existing_type=sa.INTEGER(),
        type_=sa.BigInteger(),
        existing_nullable=False,
    )
    op.alter_column(
        "profiles",
        "general_search_requests",
        existing_type=sa.INTEGER(),
        nullable=False,
    )
    op.alter_column(
        "requests",
        "author_telegram_id",
        existing_type=sa.INTEGER(),
        type_=sa.BigInteger(),
        existing_nullable=False,
    )
    op.alter_column(
        "updates",
        "user_id",
        existing_type=sa.VARCHAR(),
        type_=sa.BigInteger(),
        existing_nullable=False,
    )
    op.alter_column(
        "users",
        "telegram_id",
        existing_type=sa.INTEGER(),
        type_=sa.BigInteger(),
        existing_nullable=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "users",
        "telegram_id",
        existing_type=sa.BigInteger(),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
    op.alter_column(
        "updates",
        "user_id",
        existing_type=sa.BigInteger(),
        type_=sa.VARCHAR(),
        existing_nullable=False,
    )
    op.alter_column(
        "requests",
        "author_telegram_id",
        existing_type=sa.BigInteger(),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
    op.alter_column(
        "profiles",
        "general_search_requests",
        existing_type=sa.INTEGER(),
        nullable=True,
    )
    op.alter_column(
        "profiles",
        "user_telegram_id",
        existing_type=sa.BigInteger(),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
    # ### end Alembic commands ###
