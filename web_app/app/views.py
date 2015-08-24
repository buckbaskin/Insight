from web_app.app import app
from flask import render_template, flash, redirect, url_for
# from flask.ext.login import login_user, logout_user
from web_app.app.forms import SignupForm, EditForm
from web_app.app import db
from web_app.app.models import User

import datetime


@app.route('/')
@app.route('/index')
def index():
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
                           posts=posts)

@app.route('/create/<username>', methods=['GET','POST'])
def create_name(username):
    form = SignupForm()
    form.username.data = username
    if form.validate_on_submit():
        # create user
        user = User(form.username.data)
        db.session.add(user)
        db.session.commit()
        flash('created user '+user.t_screen_name)
        return redirect(url_for('index'))
    return render_template('user_create.html', title='Add new user', form=form)

@app.route('/create', methods=['GET','POST'])
def create():
    form = SignupForm()
    if form.validate_on_submit():
        # create user
        user = User(form.username.data)
        db.session.add(user)
        db.session.commit()
        flash('created user '+user.t_screen_name)
        return redirect(url_for('index'))
    return render_template('user_create.html', title='Add new user', form=form)


@app.route('/user/<username>/edit', methods=['GET','POST'])
def edit_user(username):
    u = User.query.filter_by(t_screen_name=username).first()  # @UndefinedVariable
    if u == None:
        flash('Twitter screenname not found for '+username)
        return redirect(url_for('create_name', username=username))
    form = EditForm()
    if form.validate_on_submit():
        u.description = form.about_me.data
        u.last_updated = datetime.datetime.utcnow()
        db.session.add(u)
        db.session.commit()
        return redirect(url_for('user', username=username))
    else:
        form = EditForm()
    return render_template('user_edit_profile.html', user=u, form=form)

@app.route('/user/<username>')
def user(username):
    u = User.query.filter_by(t_screen_name=username).first()  # @UndefinedVariable
    if u == None:
        flash('Twitter screenname not found for '+username)
        return redirect(url_for('create_name', username=username))
    posts = u.posts.all()
    return render_template('user_profile.html', user=u, posts=posts)
    
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    db.session.rollback()
    return render_template('500.html'), 500