from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
follows = Table('follows', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('followee', INTEGER),
    Column('follower', INTEGER),
)

migration_tmp = Table('migration_tmp', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('t_screen_name', VARCHAR(length=120)),
    Column('contributors', BOOLEAN),
    Column('created_at', DATETIME),
    Column('description', VARCHAR(length=400)),
    Column('favourites_count', INTEGER),
    Column('followers_count', INTEGER),
    Column('following', BOOLEAN),
    Column('friends_count', INTEGER),
    Column('t_id', INTEGER),
    Column('name', VARCHAR(length=30)),
    Column('statuses_count', INTEGER),
    Column('verified', BOOLEAN),
    Column('profile_url', VARCHAR(length=100)),
    Column('last_updated', DATETIME),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('t_screen_name', String(length=120)),
    Column('last_updated', DateTime),
    Column('contributors', Boolean),
    Column('created_at', DateTime(timezone=True)),
    Column('description', String(length=400)),
    Column('favourites_count', Integer),
    Column('followers_count', Integer),
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
    pre_meta.tables['follows'].drop()
    pre_meta.tables['migration_tmp'].drop()
    post_meta.tables['user'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['follows'].create()
    pre_meta.tables['migration_tmp'].create()
    post_meta.tables['user'].drop()
