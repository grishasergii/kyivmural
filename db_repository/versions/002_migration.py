from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
artist = Table('artist', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=50)),
    Column('nickname', String(length=50)),
    Column('url', String(length=100)),
)

mural_photo = Table('mural_photo', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('file_name', String(length=50)),
    Column('copyright_name', String(length=50)),
    Column('copyright_url', String(length=100)),
    Column('mural_id', Integer, nullable=False),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['artist'].create()
    post_meta.tables['mural_photo'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['artist'].drop()
    post_meta.tables['mural_photo'].drop()
