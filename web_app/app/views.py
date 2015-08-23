from web_app.app import app
from flask import render_template, flash, redirect, url_for
# from flask.ext.login import login_user, logout_user
from web_app.app.forms import SignupForm
from web_app.app import db
from web_app.app.models import User


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

@app.route('/create', methods=['GET','POST'])
def create():
    form = SignupForm()
    if form.validate_on_submit():
        # create user
        pass
    return render_template('user_create.html', title='Add new user', form=form)

@app.route('/user/<username>')
def user(username):
    u = User.query.filter_by(t_screen_name=username)  # @UndefinedVariable
    if u == None:
        flash('Twitter screenname not found for '+username)
        return redirect(url_for('index'))
    posts = [
        { 
            'author': user, 
            'body': 'Test user post 1' 
        },
        { 
            'author': user, 
            'body': 'TEst user post 2' 
        }
    ]
    return render_template('user.html', user=u, posts=posts)
    
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    db.session.rollback()
    return render_template('500.html'), 500