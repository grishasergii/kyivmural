#!web_py/bin/python
from migrate.versioning import api
from app import db
import os.path
from config import config
from app import create_app
from flask.ext.sqlalchemy import SQLAlchemy


config_name = os.getenv('FLASK_CONFIG') or 'default'
configuration = config[config_name]
SQLALCHEMY_DATABASE_URI = configuration.SQLALCHEMY_DATABASE_URI
SQLALCHEMY_MIGRATE_REPO = configuration.SQLALCHEMY_MIGRATE_REPO
app = create_app(config_name)

db = SQLAlchemy(app)

if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
    api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
    api.version_control(SQLALCHEMY_DATABASE_URI,
                        SQLALCHEMY_MIGRATE_REPO)
else:
    api.version_control(SQLALCHEMY_DATABASE_URI,
                        SQLALCHEMY_MIGRATE_REPO,
                        api.version(SQLALCHEMY_MIGRATE_REPO))