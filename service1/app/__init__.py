from flask import Flask

server = Flask(__name__)
server.config['SERVER_NAME'] = '127.0.0.1:5001'

from app import endpoints
