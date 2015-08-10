from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from web_app.config import server_config

app = Flask(__name__)
app.config.from_object(server_config)
db = SQLAlchemy(app)

from web_app.app import views, models

if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('tmp/web_app.log','a',1*1024*1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s: %(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('Insight web_app startup')