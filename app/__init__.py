from flask import Flask

server = Flask(__name__)

from Insight.app import views
