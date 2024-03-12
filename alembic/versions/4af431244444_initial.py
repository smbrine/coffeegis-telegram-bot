"""initial

Revision ID: 4af431244444
Revises: d4a1479c4474
Create Date: 2024-03-12 18:44:50.931851

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "4af431244444"
down_revision: Union[str, None] = "d4a1479c4474"
branch_labels: Union[str, Sequence[str], None] = (
    None
)
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column(
            "telegram_id",
            sa.BigInteger(),
            nullable=False,
        ),
        sa.Column(
            "is_bot", sa.Boolean(), nullable=True
        ),
        sa.Column(
            "first_name",
            sa.String(),
            nullable=True,
        ),
        sa.Column(
            "last_name",
            sa.String(),
            nullable=True,
        ),
        sa.Column(
            "username", sa.String(), nullable=True
        ),
        sa.Column(
            "language_code",
            sa.String(),
            nullable=True,
        ),
        sa.Column(
            "is_premium",
            sa.Boolean(),
            nullable=True,
        ),
        sa.Column(
            "id", sa.String(), nullable=False
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_users_telegram_id"),
        "users",
        ["telegram_id"],
        unique=True,
    )
    op.create_table(
        "profiles",
        sa.Column(
            "user_telegram_id",
            sa.BigInteger(),
            nullable=False,
        ),
        sa.Column(
            "phone",
            sa.BigInteger(),
            nullable=True,
        ),
        sa.Column(
            "email", sa.String(), nullable=True
        ),
        sa.Column(
            "new_cafes_notify",
            sa.Boolean(),
            nullable=True,
        ),
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=True,
        ),
        sa.Column(
            "general_search_requests",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "is_phone_confirmed",
            sa.Integer(),
            nullable=True,
        ),
        sa.Column(
            "id", sa.String(), nullable=False
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["user_telegram_id"],
            ["users.telegram_id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_telegram_id"),
    )
    op.create_index(
        op.f("ix_profiles_email"),
        "profiles",
        ["email"],
        unique=True,
    )
    op.create_index(
        op.f("ix_profiles_phone"),
        "profiles",
        ["phone"],
        unique=True,
    )
    op.create_table(
        "updates",
        sa.Column(
            "user_id",
            sa.BigInteger(),
            nullable=False,
        ),
        sa.Column(
            "update_id",
            sa.Integer(),
            nullable=True,
        ),
        sa.Column(
            "update_type",
            sa.String(),
            nullable=False,
        ),
        sa.Column(
            "update_data",
            postgresql.JSONB(
                astext_type=sa.Text()
            ),
            nullable=True,
        ),
        sa.Column(
            "id", sa.String(), nullable=False
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.telegram_id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "requests",
        sa.Column(
            "author_telegram_id",
            sa.BigInteger(),
            nullable=False,
        ),
        sa.Column(
            "request_type",
            sa.String(),
            nullable=False,
        ),
        sa.Column(
            "contents",
            postgresql.JSONB(
                astext_type=sa.Text()
            ),
            nullable=False,
        ),
        sa.Column(
            "id", sa.String(), nullable=False
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["author_telegram_id"],
            ["profiles.user_telegram_id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("requests")
    op.drop_table("updates")
    op.drop_index(
        op.f("ix_profiles_phone"),
        table_name="profiles",
    )
    op.drop_index(
        op.f("ix_profiles_email"),
        table_name="profiles",
    )
    op.drop_table("profiles")
    op.drop_index(
        op.f("ix_users_telegram_id"),
        table_name="users",
    )
    op.drop_table("users")
    # ### end Alembic commands ###
