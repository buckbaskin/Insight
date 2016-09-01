from flask import Blueprint

blueprint = Blueprint('twitter_api', __name__, template_folder='templates', static_folder='static')

from app.twitter_api import endpoints
