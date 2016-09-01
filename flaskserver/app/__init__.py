from flask import Flask
import requests
requests_service = requests.Session()

server = Flask(__name__)
server.config['SERVER_NAME'] = '127.0.0.1:5000'

from app.simple_blueprint import simple_page
from app import home, clicktrack, performance, sql

server.register_blueprint(simple_page, url_prefix='/nicole')
server.register_blueprint(home.blueprint, url_prefix='')
server.register_blueprint(clicktrack.blueprint, url_prefix='/click')
server.register_blueprint(performance.blueprint, url_prefix='/performance')
server.register_blueprint(sql.blueprint, url_prefix='')

print('app.url_map: %s' % (server.url_map,))

# from app.clicktrack import endpoints
# from app.performance import endpoints
# from app.sql import endpoints
# from app.twitter_api import endpoints
