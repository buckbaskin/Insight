from web_app.app import app
from flask import render_template
from web_app.app import db
from web_app.app.routes.core_routes import core_index
from web_app.app.routes.user_routes import user_login

@app.route('/')
@app.route('/index')

def index():
    core_index()
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    user_login()

# Default error handling

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    db.session.rollback()
    return render_template('500.html'), 500