from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('t_screen_name', String(length=120)),
    Column('user_created', DateTime),
    Column('contributors', Boolean),
    Column('created_at', DateTime(timezone=True)),
    Column('description', String(length=400)),
    Column('favourites_count', Integer),
    Column('followers_count', Integer),
    Column('following', Boolean),
    Column('friends_count', Integer),
    Column('t_id', Integer),
    Column('name', String(length=30)),
    Column('statuses_count', Integer),
    Column('verified', Boolean),
    Column('profile_url', String(length=100)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['user'].columns['user_created'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['user'].columns['user_created'].drop()
