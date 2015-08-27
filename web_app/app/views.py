from web_app.app import app
from flask import render_template, flash, redirect, url_for
# from flask.ext.login import login_user, logout_user
from web_app.app.forms import SignupForm, EditForm, PostForm
from web_app.app import db
from web_app.app.models import User, Post
from web_app.config.user_config import POSTS_PER_PAGE
from web_app.analytics import analyze

import datetime
from sqlalchemy import desc


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/index/<int:page>', methods=['GET', 'POST'])
@app.route('/index/<int:page>/<int:session>', methods=['GET', 'POST'])
@analyze
def index(page=1, session=None):
    flash('session: '+str(session))
    print 'index/'+str(page)+' called'
    if(page > POSTS_PER_PAGE):
        return redirect(url_for('index', page=1))
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page,POSTS_PER_PAGE,False) # @UndefinedVariable
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, timestamp=datetime.datetime.utcnow(), author=User('indexUser'))
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    return render_template('index.html',
                           title='Home',
                           posts=posts,
                           form=form,
                           session=session)

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
    posts = u.posts.order_by(desc(Post.timestamp)).paginate(1,POSTS_PER_PAGE,False).items
    return render_template('user_profile.html', user=u, posts=posts)
    
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    db.session.rollback()
    return render_template('500.html'), 500