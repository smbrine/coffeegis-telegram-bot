"""fixing user preferences

Revision ID: 24fb2a6021ee
Revises: 01ef42fbba01
Create Date: 2024-05-20 14:19:17.849239

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "24fb2a6021ee"
down_revision: Union[str, None] = "01ef42fbba01"
branch_labels: Union[str, Sequence[str], None] = (
    None
)
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
