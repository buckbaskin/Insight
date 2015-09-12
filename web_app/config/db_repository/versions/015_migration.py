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

session = Table('session', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('start', DATETIME),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['page_load'].drop()
    pre_meta.tables['session'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['page_load'].create()
    pre_meta.tables['session'].create()