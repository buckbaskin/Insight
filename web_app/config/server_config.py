import os

basedir = os.path.abspath(os.path.dirname(__file__))

from web_app.config import secret_config

DEBUG = True
PORT = 5000
HOST = '127.0.0.1'

WTF_CSRF_ENABLED = True
SECRET_KEY = secret_config.SECRET_KEY
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')