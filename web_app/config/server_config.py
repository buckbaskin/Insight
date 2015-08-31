import os
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

from web_app.config import secret_config

DEBUG = True
PORT = 5000
HOST = '0.0.0.0'

WTF_CSRF_ENABLED = True
SECRET_KEY = secret_config.SECRET_KEY
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_DATABASE_URL = 'postgresql://localhost/' + os.path.join(basedir, 'psql_app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
