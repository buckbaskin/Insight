from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

import config

from rq import Queue
from scripts.redis_worker import conn

server = Flask(__name__)
server.config.from_object(config)
db = SQLAlchemy(server)
q = Queue(connection=conn) # other Queue, doesn't care about rate limit
t_q = Queue(connection=conn) # Twitter Queue, knows about rate limit

from app import models
from app import routes


if not server.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('tmp/web_app.log','a',1*1024*1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s: %(lineno)d]'))
    server.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    server.logger.addHandler(file_handler)
    server.logger.info('Insight web_app startup')