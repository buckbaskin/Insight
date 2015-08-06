from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from web_app.config import server_config

app = Flask(__name__)
app.config.from_object(server_config)
db = SQLAlchemy(app)

from web_app.app import views, models
