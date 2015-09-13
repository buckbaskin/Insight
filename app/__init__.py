from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

import config

from rq import Queue
from scripts.redis_worker import conn

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)
q = Queue(connection=conn) # other Queue, doesn't care about rate limit
t_q = Queue(connection=conn) # Twitter Queue, knows about rate limit

from app import models
from app import routes

if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('tmp/web_app.log','a',1*1024*1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s: %(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('Insight web_app startup')