from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
artist = Table('artist', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR(length=50)),
    Column('nickname', VARCHAR(length=50)),
    Column('url', VARCHAR(length=100)),
)

language = Table('language', pre_meta,
    Column('code', VARCHAR(length=2), primary_key=True, nullable=False),
    Column('name', VARCHAR(length=20)),
)

mural = Table('mural', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('lat', FLOAT, nullable=False),
    Column('lng', FLOAT, nullable=False),
)

mural_photo = Table('mural_photo', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('file_name', VARCHAR(length=50)),
    Column('copyright_name', VARCHAR(length=50)),
    Column('copyright_url', VARCHAR(length=100)),
    Column('mural_id', INTEGER, nullable=False),
)

artists = Table('artists', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=50)),
    Column('nickname', String(length=50)),
    Column('url', String(length=100)),
)

languages = Table('languages', post_meta,
    Column('code', String(length=2), primary_key=True, nullable=False),
    Column('name', String(length=20)),
)

muralphotos = Table('muralphotos', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('file_name', String(length=50)),
    Column('copyright_name', String(length=50)),
    Column('copyright_url', String(length=100)),
    Column('mural_id', Integer, nullable=False),
)

murals = Table('murals', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('lat', Float, nullable=False),
    Column('lng', Float, nullable=False),
)

roles = Table('roles', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
)

users = Table('users', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('username', String(length=64)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['artist'].drop()
    pre_meta.tables['language'].drop()
    pre_meta.tables['mural'].drop()
    pre_meta.tables['mural_photo'].drop()
    post_meta.tables['artists'].create()
    post_meta.tables['languages'].create()
    post_meta.tables['muralphotos'].create()
    post_meta.tables['murals'].create()
    post_meta.tables['roles'].create()
    post_meta.tables['users'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['artist'].create()
    pre_meta.tables['language'].create()
    pre_meta.tables['mural'].create()
    pre_meta.tables['mural_photo'].create()
    post_meta.tables['artists'].drop()
    post_meta.tables['languages'].drop()
    post_meta.tables['muralphotos'].drop()
    post_meta.tables['murals'].drop()
    post_meta.tables['roles'].drop()
    post_meta.tables['users'].drop()
