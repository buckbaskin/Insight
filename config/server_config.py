import os
basedir = os.path.abspath(os.path.dirname(__file__))

from config.secret_config import SECRET_KEY

DEBUG = True
PORT = 5000
HOST = '0.0.0.0'

WTF_CSRF_ENABLED = True
SQLALCHEMY_DATABASE_URI = 'postgresql:///' + 'psql_app'# os.path.join(basedir, 'psql_app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')