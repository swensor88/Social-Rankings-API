"""initial schema

Revision ID: 20260527_0001
Revises:
Create Date: 2026-05-27

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "20260527_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    download_type_enum = sa.Enum("api", "web", "s3", name="download_type_enum")
    download_frequency_enum = sa.Enum(
        "hourly", "daily", "weekly", name="download_frequency_enum"
    )

    download_type_enum.create(op.get_bind(), checkfirst=True)
    download_frequency_enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "political_body",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
    )

    op.create_table(
        "politicians",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("political_body_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("current_position", sa.Text(), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.ForeignKeyConstraint(["political_body_id"], ["political_body.id"]),
    )

    op.create_table(
        "social_channel",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("audience_type", sa.Text(), nullable=False),
        sa.Column("download_type", download_type_enum, nullable=False),
        sa.Column("download_frequency", download_frequency_enum, nullable=False),
    )

    op.create_table(
        "accounts",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("politician_id", sa.Integer(), nullable=False),
        sa.Column("social_channel_id", sa.Integer(), nullable=False),
        sa.Column("total_audience", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["politician_id"], ["politicians.id"]),
        sa.ForeignKeyConstraint(["social_channel_id"], ["social_channel.id"]),
    )

    op.create_index(op.f("ix_political_body_id"), "political_body", ["id"], unique=False)
    op.create_index(op.f("ix_politicians_id"), "politicians", ["id"], unique=False)
    op.create_index(op.f("ix_social_channel_id"), "social_channel", ["id"], unique=False)
    op.create_index(op.f("ix_accounts_id"), "accounts", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_accounts_id"), table_name="accounts")
    op.drop_index(op.f("ix_social_channel_id"), table_name="social_channel")
    op.drop_index(op.f("ix_politicians_id"), table_name="politicians")
    op.drop_index(op.f("ix_political_body_id"), table_name="political_body")

    op.drop_table("accounts")
    op.drop_table("social_channel")
    op.drop_table("politicians")
    op.drop_table("political_body")

    download_frequency_enum = sa.Enum(
        "hourly", "daily", "weekly", name="download_frequency_enum"
    )
    download_type_enum = sa.Enum("api", "web", "s3", name="download_type_enum")

    download_frequency_enum.drop(op.get_bind(), checkfirst=True)
    download_type_enum.drop(op.get_bind(), checkfirst=True)
