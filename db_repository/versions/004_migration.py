from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
artist_translation = Table('artist_translation', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('artist_id', Integer, nullable=False),
    Column('language_code', String(length=2), nullable=False),
    Column('about', Text),
)

language = Table('language', post_meta,
    Column('code', String(length=2), primary_key=True, nullable=False),
    Column('name', String(length=20)),
)

mural_translation = Table('mural_translation', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('mural_id', Integer, nullable=False),
    Column('language_code', String(length=2), nullable=False),
    Column('description', Text),
    Column('name', String(length=50)),
    Column('address', String(length=100)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['artist_translation'].create()
    post_meta.tables['language'].create()
    post_meta.tables['mural_translation'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['artist_translation'].drop()
    post_meta.tables['language'].drop()
    post_meta.tables['mural_translation'].drop()
