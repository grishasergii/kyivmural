#!web_py/bin/python
import os
from migrate.versioning import api
from config import config

config_ = config[os.getenv('FLASK_CONFIG') or 'default']
api.upgrade(config_.SQLALCHEMY_DATABASE_URI, config_.SQLALCHEMY_MIGRATE_REPO)
v = api.db_version(config_.SQLALCHEMY_DATABASE_URI, config_.SQLALCHEMY_MIGRATE_REPO)
print('Current database version: ' + str(v))