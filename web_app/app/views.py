from web_app.app import app
from flask import render_template
# from flask import flash, redirect, url_for
# from flask.ext.login import login_user, logout_user
# from web_app.app.forms import LoginForm, SignupForm
from web_app.app import db
# from web_app.app.models import User


@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'fakeBuck'}  # fake user
    posts = [  # fake array of posts
        { 
            'author': {'nickname': 'John'}, 
            'body': 'Beautiful day in Portland!' 
        },
        { 
            'author': {'nickname': 'Susan'}, 
            'body': 'The Avengers movie was so cool!' 
        }
    ]
    return render_template('index.html',
                           title='Home',
                           user=user, 
                           posts=posts)
    
def user():
    pass
    
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    db.session.rollback()
    return render_template('500.html'), 500