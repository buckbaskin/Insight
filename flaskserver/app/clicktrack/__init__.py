from flask import Blueprint

blueprint = Blueprint('clicktrack', __name__, template_folder='templates', static_folder='static')

from app.clicktrack import endpoints

