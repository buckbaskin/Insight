from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from web_app.config import server_config

app = Flask(__name__)
app.config.from_object(server_config)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

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
    
@login_manager.user_loader
def load_user(user_id):
    print 'Possible error with undefined User or query'
    from web_app.app.models import User
    return User.query.get(int(user_id)) # @UndefinedVariable query