from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
artist_translations = Table('artist_translations', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('artist_id', INTEGER, nullable=False),
    Column('language_code', VARCHAR(length=2), nullable=False),
    Column('about', TEXT),
)

artists = Table('artists', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR(length=50)),
    Column('nickname', VARCHAR(length=50)),
    Column('url', VARCHAR(length=100)),
)

languages = Table('languages', pre_meta,
    Column('code', VARCHAR(length=2), primary_key=True, nullable=False),
    Column('name', VARCHAR(length=20)),
)

mural_artist = Table('mural_artist', pre_meta,
    Column('mural_id', INTEGER, primary_key=True, nullable=False),
    Column('artist_id', INTEGER, primary_key=True, nullable=False),
)

mural_photos = Table('mural_photos', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('file_name', VARCHAR(length=100)),
    Column('copyright_name', VARCHAR(length=50)),
    Column('copyright_url', VARCHAR(length=100)),
    Column('mural_id', INTEGER, nullable=False),
)

mural_translations = Table('mural_translations', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('mural_id', INTEGER, nullable=False),
    Column('language_code', VARCHAR(length=2), nullable=False),
    Column('description', TEXT),
    Column('name', VARCHAR(length=50)),
    Column('address', VARCHAR(length=100)),
)

murals = Table('murals', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('lat', FLOAT, nullable=False),
    Column('lng', FLOAT, nullable=False),
)

roles = Table('roles', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR(length=64)),
)

users = Table('users', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('username', VARCHAR(length=64)),
    Column('role_id', INTEGER),
    Column('password_hash', VARCHAR(length=128)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['artist_translations'].drop()
    pre_meta.tables['artists'].drop()
    pre_meta.tables['languages'].drop()
    pre_meta.tables['mural_artist'].drop()
    pre_meta.tables['mural_photos'].drop()
    pre_meta.tables['mural_translations'].drop()
    pre_meta.tables['murals'].drop()
    pre_meta.tables['roles'].drop()
    pre_meta.tables['users'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['artist_translations'].create()
    pre_meta.tables['artists'].create()
    pre_meta.tables['languages'].create()
    pre_meta.tables['mural_artist'].create()
    pre_meta.tables['mural_photos'].create()
    pre_meta.tables['mural_translations'].create()
    pre_meta.tables['murals'].create()
    pre_meta.tables['roles'].create()
    pre_meta.tables['users'].create()
