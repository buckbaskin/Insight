from flask import Blueprint

blueprint = Blueprint('performance', __name__)

from app.performance.decorator import speed_test2, mem_test, performance
del decorator

from app.performance import endpoints

