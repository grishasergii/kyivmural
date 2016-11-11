#!web_py/bin/python
import os
import imp
from migrate.versioning import api
from config import config
from app import create_app
from flask.ext.sqlalchemy import SQLAlchemy


config_name = os.getenv('FLASK_CONFIG') or 'default'
configuration = config[config_name]
SQLALCHEMY_DATABASE_URI = configuration.SQLALCHEMY_DATABASE_URI
SQLALCHEMY_MIGRATE_REPO = configuration.SQLALCHEMY_MIGRATE_REPO
app = create_app(config_name)

db = SQLAlchemy(app)

v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
migration = SQLALCHEMY_MIGRATE_REPO + ('/versions/%03d_migration.py' % (v+1))
tmp_module = imp.new_module('old_model')
old_module = api.create_model(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
exec(old_module, tmp_module.__dict__)
script = api.make_update_script_for_model(SQLALCHEMY_DATABASE_URI,
                                          SQLALCHEMY_MIGRATE_REPO,
                                          tmp_module.meta,
                                          db.metadata)
open(migration, "wt").write(script)
api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
print('New migration saved as ' + migration)
print('Current database version: ' + str(v))
