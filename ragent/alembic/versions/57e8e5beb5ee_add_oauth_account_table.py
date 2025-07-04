"""add oauth_account table

Revision ID: 57e8e5beb5ee
Revises: 9994af2a3ca2
Create Date: 2025-06-30 14:13:04.952181

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '57e8e5beb5ee'
down_revision = '9994af2a3ca2'
branch_labels = None
depends_on = None

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('oauth_accounts', sa.Column('user_id', sa.Integer(), nullable=False))
    op.add_column('oauth_accounts', sa.Column('provider', sa.String(length=50), nullable=False))
    op.add_column('oauth_accounts', sa.Column('provider_user_id', sa.String(length=255), nullable=False))
    op.add_column('oauth_accounts', sa.Column('access_token', sa.String(length=512), nullable=True))
    op.add_column('oauth_accounts', sa.Column('refresh_token', sa.String(length=512), nullable=True))
    op.add_column('oauth_accounts', sa.Column('token_expiry', sa.DateTime(), nullable=True))
    op.add_column('oauth_accounts', sa.Column('scope', sa.ARRAY(sa.String()), nullable=True))
    op.add_column('oauth_accounts', sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.add_column('oauth_accounts', sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.create_foreign_key(None, 'oauth_accounts', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'oauth_accounts', type_='foreignkey')
    op.drop_column('oauth_accounts', 'updated_at')
    op.drop_column('oauth_accounts', 'created_at')
    op.drop_column('oauth_accounts', 'scope')
    op.drop_column('oauth_accounts', 'token_expiry')
    op.drop_column('oauth_accounts', 'refresh_token')
    op.drop_column('oauth_accounts', 'access_token')
    op.drop_column('oauth_accounts', 'provider_user_id')
    op.drop_column('oauth_accounts', 'provider')
    op.drop_column('oauth_accounts', 'user_id')
    # ### end Alembic commands ###