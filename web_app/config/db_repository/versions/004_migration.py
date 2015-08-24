from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
follows = Table('follows', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('follower', Integer),
    Column('followee', Integer),
)

user = Table('user', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('t_username', VARCHAR(length=120)),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('t_screen_name', String(length=120)),
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
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['follows'].columns['followee'].create()
    post_meta.tables['follows'].columns['follower'].create()
    pre_meta.tables['user'].columns['t_username'].drop()
    post_meta.tables['user'].columns['contributors'].create()
    post_meta.tables['user'].columns['created_at'].create()
    post_meta.tables['user'].columns['description'].create()
    post_meta.tables['user'].columns['favourites_count'].create()
    post_meta.tables['user'].columns['followers_count'].create()
    post_meta.tables['user'].columns['following'].create()
    post_meta.tables['user'].columns['friends_count'].create()
    post_meta.tables['user'].columns['name'].create()
    post_meta.tables['user'].columns['statuses_count'].create()
    post_meta.tables['user'].columns['t_id'].create()
    post_meta.tables['user'].columns['t_screen_name'].create()
    post_meta.tables['user'].columns['verified'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['follows'].columns['followee'].drop()
    post_meta.tables['follows'].columns['follower'].drop()
    pre_meta.tables['user'].columns['t_username'].create()
    post_meta.tables['user'].columns['contributors'].drop()
    post_meta.tables['user'].columns['created_at'].drop()
    post_meta.tables['user'].columns['description'].drop()
    post_meta.tables['user'].columns['favourites_count'].drop()
    post_meta.tables['user'].columns['followers_count'].drop()
    post_meta.tables['user'].columns['following'].drop()
    post_meta.tables['user'].columns['friends_count'].drop()
    post_meta.tables['user'].columns['name'].drop()
    post_meta.tables['user'].columns['statuses_count'].drop()
    post_meta.tables['user'].columns['t_id'].drop()
    post_meta.tables['user'].columns['t_screen_name'].drop()
    post_meta.tables['user'].columns['verified'].drop()
