"""empty message

Revision ID: 0020_assets_user_id
Revises: 0019_add_games_extra_metadata
Create Date: 2024-02-01 17:08:02.103046

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0020_assets_user_id"
down_revision = "0019_add_games_extra_metadata"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("saves", schema=None) as batch_op:
        batch_op.add_column(sa.Column("user_id", sa.Integer(), nullable=False))
        batch_op.create_foreign_key(
            "saves_user_FK", "users", ["user_id"], ["id"], ondelete="CASCADE"
        )

    with op.batch_alter_table("screenshots", schema=None) as batch_op:
        batch_op.add_column(sa.Column("user_id", sa.Integer(), nullable=False))
        batch_op.create_foreign_key(
            "screenshots_user_FK", "users", ["user_id"], ["id"], ondelete="CASCADE"
        )

    with op.batch_alter_table("states", schema=None) as batch_op:
        batch_op.add_column(sa.Column("user_id", sa.Integer(), nullable=False))
        batch_op.create_foreign_key(
            "states_user_FK", "users", ["user_id"], ["id"], ondelete="CASCADE"
        )

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("states", schema=None) as batch_op:
        batch_op.drop_constraint("states_user_FK", type_="foreignkey")
        batch_op.drop_column("user_id")

    with op.batch_alter_table("screenshots", schema=None) as batch_op:
        batch_op.drop_constraint("screenshots_user_FK", type_="foreignkey")
        batch_op.drop_column("user_id")

    with op.batch_alter_table("saves", schema=None) as batch_op:
        batch_op.drop_constraint("saves_user_FK", type_="foreignkey")
        batch_op.drop_column("user_id")

    # ### end Alembic commands ###