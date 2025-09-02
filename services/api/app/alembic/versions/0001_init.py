
"""initial schema

Revision ID: 0001_init
Revises: 
Create Date: 2025-09-01 00:00:00.000000
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '0001_init'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS pgcrypto")

    op.create_table('sources',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.Text(), nullable=False),
        sa.Column('kind', sa.Text(), nullable=False),
        sa.Column('url', sa.Text()),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'))
    )

    op.create_table('artifacts',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('source_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('sources.id', ondelete="SET NULL")),
        sa.Column('title', sa.Text()),
        sa.Column('url', sa.Text()),
        sa.Column('author', sa.Text()),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'))
    )

    op.create_table('notes',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('artifact_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('artifacts.id', ondelete="CASCADE")),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('llm', sa.Text()),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'))
    )

    op.create_table('tags',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.Text(), unique=True, nullable=False)
    )

    op.create_table('artifact_tags',
        sa.Column('artifact_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('artifacts.id', ondelete="CASCADE"), primary_key=True),
        sa.Column('tag_id', sa.Integer(), sa.ForeignKey('tags.id', ondelete="CASCADE"), primary_key=True)
    )

    op.create_table('embeddings',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('artifact_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('artifacts.id', ondelete="CASCADE")),
        sa.Column('vector', postgresql.ARRAY(sa.REAL)),
        sa.Column('model', sa.Text()),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'))
    )

    op.create_table('events',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('topic', sa.Text(), nullable=False),
        sa.Column('payload', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'))
    )

def downgrade() -> None:
    op.drop_table('events')
    op.drop_table('embeddings')
    op.drop_table('artifact_tags')
    op.drop_table('tags')
    op.drop_table('notes')
    op.drop_table('artifacts')
    op.drop_table('sources')
