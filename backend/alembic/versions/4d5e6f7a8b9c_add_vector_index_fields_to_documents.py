"""add_vector_index_fields_to_documents

Revision ID: 4d5e6f7a8b9c
Revises: 3c4d5e6f7a8b
Create Date: 2026-06-21 22:55:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4d5e6f7a8b9c'
down_revision = '3c4d5e6f7a8b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('documents', sa.Column('vector_indexed', sa.Boolean(), server_default='false', nullable=True))
    op.add_column('documents', sa.Column('vector_indexed_at', sa.DateTime(), nullable=True))
    op.add_column('documents', sa.Column('faiss_document_id', sa.String(length=255), nullable=True))
    op.add_column('documents', sa.Column('vector_count', sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column('documents', 'vector_count')
    op.drop_column('documents', 'faiss_document_id')
    op.drop_column('documents', 'vector_indexed_at')
    op.drop_column('documents', 'vector_indexed')
