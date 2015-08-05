from web_app.app import app
from flask import render_template

@app.route('/')
@app.route('/index')

def index():
    user = {'nickname': 'Buck'}  # fake user
    return render_template('index.html',
                           title='Home',
                           user=user)