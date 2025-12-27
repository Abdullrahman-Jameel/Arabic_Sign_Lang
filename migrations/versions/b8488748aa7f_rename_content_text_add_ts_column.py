from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'b8488748aa7f'
down_revision = '1405622a3538'
branch_labels = None
depends_on = None

def upgrade():
    # 1️⃣ rename column `content` → `text`
    with op.batch_alter_table('conversation') as batch_op:
        batch_op.alter_column('content',
                              new_column_name='text',
                              existing_type=sa.TEXT(),
                              nullable=False)

        # 2️⃣ add timestamp column
        batch_op.add_column(sa.Column('ts', sa.DateTime(), nullable=True))

    # 3️⃣ fill ts for older rows so it’s never NULL
    op.execute("UPDATE conversation SET ts = CURRENT_TIMESTAMP WHERE ts IS NULL")


def downgrade():
    with op.batch_alter_table('conversation') as batch_op:
        batch_op.alter_column('text',
                              new_column_name='content',
                              existing_type=sa.TEXT(),
                              nullable=False)
        batch_op.drop_column('ts')
