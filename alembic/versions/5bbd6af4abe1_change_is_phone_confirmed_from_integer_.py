"""change_is_phone_confirmed_from_integer

Revision ID: 5bbd6af4abe1
Revises: 1ce046c47f92
Create Date: 2024-05-15 19:17:12.812474

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "5bbd6af4abe1"
down_revision = "1ce046c47f92"
branch_labels: Union[str, Sequence[str], None] = (
    None
)
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Step 1: Add a temporary column to store the boolean values
    op.add_column(
        "profiles",
        sa.Column(
            "is_phone_confirmed_temp",
            sa.Boolean,
            nullable=True,
        ),
    )

    # Step 2: Populate the temporary column with converted values
    op.execute(
        """
    UPDATE public.profiles
    SET is_phone_confirmed_temp = CASE
        WHEN is_phone_confirmed = 0 THEN FALSE
        ELSE TRUE
    END
    """
    )

    # Step 3: Drop the original column
    op.drop_column(
        "profiles", "is_phone_confirmed"
    )

    # Step 4: Rename the temporary column to the original column name
    op.alter_column(
        "profiles",
        "is_phone_confirmed_temp",
        new_column_name="is_phone_confirmed",
    )


def downgrade():
    # Step 1: Add a temporary column to store the integer values
    op.add_column(
        "profiles",
        sa.Column(
            "is_phone_confirmed_temp",
            sa.Integer,
            nullable=True,
        ),
    )

    # Step 2: Populate the temporary column with converted values
    op.execute(
        """
    UPDATE public.profiles
    SET is_phone_confirmed_temp = CASE
        WHEN is_phone_confirmed THEN 1
        ELSE 0
    END
    """
    )

    # Step 3: Drop the boolean column
    op.drop_column(
        "profiles", "is_phone_confirmed"
    )

    # Step 4: Rename the temporary column to the original column name
    op.alter_column(
        "profiles",
        "is_phone_confirmed_temp",
        new_column_name="is_phone_confirmed",
    )
