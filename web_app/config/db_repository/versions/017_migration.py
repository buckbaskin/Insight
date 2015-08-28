from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
page_load = Table('page_load', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('time', DATETIME),
    Column('page_id', VARCHAR(length=80)),
    Column('session_id', INTEGER),
)

page_load = Table('page_load', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('time', DateTime),
    Column('page_id', String(length=80)),
    Column('trace_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['page_load'].columns['session_id'].drop()
    post_meta.tables['page_load'].columns['trace_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['page_load'].columns['session_id'].create()
    post_meta.tables['page_load'].columns['trace_id'].drop()
