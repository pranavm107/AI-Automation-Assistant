"""add_embedding_fields_to_documents

Revision ID: 3c4d5e6f7a8b
Revises: 2b3c4d5e6f7a
Create Date: 2026-06-21 22:45:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c4d5e6f7a8b'
down_revision = '2b3c4d5e6f7a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('documents', sa.Column('embeddings_generated', sa.Boolean(), server_default='false', nullable=True))
    op.add_column('documents', sa.Column('embeddings_generated_at', sa.DateTime(), nullable=True))
    op.add_column('documents', sa.Column('embedding_model', sa.String(length=100), nullable=True))
    op.add_column('documents', sa.Column('embedding_dimension', sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column('documents', 'embedding_dimension')
    op.drop_column('documents', 'embedding_model')
    op.drop_column('documents', 'embeddings_generated_at')
    op.drop_column('documents', 'embeddings_generated')
