import imp
from migrate.versioning import api
from web_app.app import db
from web_app.config.server_config import SQLALCHEMY_DATABASE_URI as db_uri
from web_app.config.server_config import SQLALCHEMY_MIGRATE_REPO as mig_repo

v = api.db_version(db_uri, mig_repo)
migration = mig_repo + ('/versions/%03d_migration.py' % (v+1))
tmp_module = imp.new_module('old_model')
old_model = api.create_model(db_uri, mig_repo)
exec(old_model, tmp_module.__dict__)
script = api.make_update_script_for_model(db_uri, mig_repo, tmp_module.meta, db.metadata)
open(migration, "wt").write(script)
api.upgrade(db_uri, mig_repo)
v = api.db_version(db_uri, mig_repo)
print('New migration saved as ' + migration)
print('Current database version: ' + str(v))