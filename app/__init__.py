from flask import Flask
import requests
requests_service = requests.Session()

server = Flask(__name__)
server.config['SERVER_NAME'] = '127.0.0.1:5000'

from Insight.app import views
from Insight.clicktrack import endpoints
from Insight.performance import endpoints
from Insight.sql import endpoints

