from migrate.versioning import api
from web_app.app import db
from web_app.config.server_config import SQLALCHEMY_DATABASE_URI as db_uri
from web_app.config.server_config import SQLALCHEMY_MIGRATE_REPO as mig_repo

import os.path
db.create_all()

if not os.path.exists(mig_repo):
    print 'mig_repo does not exist'
    api.create(mig_repo, 'database repository')
    print 'created mig_repo'
    api.version_control(db_uri, mig_repo)
    print 'added version control'
else:
    api.version_control(db_uri, mig_repo, api.version(mig_repo))
    print 'added version control'