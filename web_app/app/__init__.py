from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from web_app.config.server_config import config as server_config

app = Flask(__name__)
app.config.update(server_config)
db = SQLAlchemy(app)

from web_app.app import views, models
