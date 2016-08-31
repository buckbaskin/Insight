from flask import Flask
import requests
requests_service = requests.Session()

server = Flask(__name__)
server.config['SERVER_NAME'] = '127.0.0.1:5000'

from app.simple_blueprint import simple_page

server.register_blueprint(simple_page, url_prefix='/nicole')

from app.home import endpoints
from app.clicktrack import endpoints
from app.performance import endpoints
from app.sql import endpoints
from app.twitter_api import endpoints

