import sys
sys.path.append('/home/buck/Github/Insight')

from web_app.app import app
from flask import render_template, flash, redirect, url_for
from flask import jsonify
# from flask.ext.login import login_user, logout_user
from web_app.app.forms import SignupForm, EditForm, PostForm
from web_app.app.forms import ReqForm
from web_app.app import db, q
from web_app.app.models import User, Post, PageLoad #, Trace
from web_app.app.models import Result
from web_app.app.tasks import count_and_save_words
from web_app.config.user_config import POSTS_PER_PAGE
from web_app.analytics import analyze

import datetime
from sqlalchemy import desc

# Comment for cleanup
# import requests
# from stop_words import stops
# from collections import Counter
# from bs4 import BeautifulSoup
# import re
# import nltk
import operator

from web_app.scripts.redis_worker import conn
from rq.job import Job


@app.route('/', methods=['GET', 'POST'])
def index2():
    flash('wrong index')
    form = ReqForm()
    results = ()
    if form.validate_on_submit():
        url = form.url.data
        job = q.enqueue_call(
            func=count_and_save_words, args=(url,), result_ttl=5000
        )
        print str(job.get_id())
    
    return render_template('index2.html',
                           form=form,
                           # errors = errors,
                           results=results)
    
@app.route('/results/<job_key>', methods=['GET'])
def get_queue_results(job_key):
    job = Job.fetch(job_key, connection=conn)
    if job.is_finished:
        result = Result.query.filter_by(id=job.result).first() 
        results = sorted(
            result.result_no_stop_words.items(),
            key=operator.itemgetter(1),
            reverse=True
        )[:10]
        return jsonify(results)
    else:
        return "Nay!", 202
    

@app.route('/index', methods=['GET', 'POST'])
@app.route('/index/<int:trace>', methods=['GET', 'POST'])
@app.route('/index/<int:trace>/<int:page>', methods=['GET', 'POST'])
@analyze
def index(trace=None, page=1):
    flash('trace: '+str(trace))
#     if(page > POSTS_PER_PAGE):
#         return redirect(url_for('index', page=1, trace=trace.serialize()))
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page,POSTS_PER_PAGE,False) # @UndefinedVariable
    form = PostForm()
    if form.validate_on_submit():
        user = User.query.filter_by(t_screen_name='indexUser').first() # @UndefinedVariable
        if not user:
            user = User('indexUser')
        post = Post(body=form.post.data, timestamp=datetime.datetime.utcnow(), author=user)
        page_name = 'index/'+str(page)+'/post'
        pg = PageLoad(trace=trace.id, page_name=page_name)
        db.session.add(post)
        db.session.add(pg)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index', page=1, trace=trace.serialize()))
    return render_template('index.html',
                           title='Home',
                           posts=posts,
                           form=form,
                           trace=trace)

@app.route('/create/<username>', methods=['GET','POST'])
@app.route('/create/<username>/<int:trace>', methods=['GET','POST'])
@analyze
def create_name(username, trace=None):
    flash('trace: '+str(trace))
    form = SignupForm()
    form.username.data = username
    if form.validate_on_submit():
        # create user
        user = User(form.username.data)
        page_name = 'create_name/'+str(username)+'/post'
        pg = PageLoad(trace=trace, page_name=page_name)
        db.session.add(user)
        db.session.add(pg)
        db.session.commit()
        flash('created user '+user.t_screen_name)
        return redirect(url_for('user', username=user.t_screen_name, trace=trace.serialize()))
    return render_template('user_create.html', title='Add new user', form=form, trace=trace)

@app.route('/create', methods=['GET','POST'])
@app.route('/create/<int:trace>', methods=['GET','POST'])
@analyze
def create(trace=None):
    flash('trace: '+str(trace))
    form = SignupForm()
    if form.validate_on_submit():
        # create user
        user = User(form.username.data)
        page_name = 'create_name/post'
        pg = PageLoad(trace=trace, page_name=page_name)
        db.session.add(user)
        db.session.add(pg)
        db.session.commit()
        flash('created user '+user.t_screen_name)
        return redirect(url_for('user', username=user.t_screen_name, trace=trace.serialize()))
    return render_template('user_create.html', title='Add new user', form=form, trace=trace)


@app.route('/user/<username>/edit', methods=['GET','POST'])
@app.route('/user/<username>/edit/<int:trace>', methods=['GET','POST'])
@analyze
def edit_user(username, trace=None):
    flash('trace: '+str(trace))
    u = User.query.filter_by(t_screen_name=username).first()  # @UndefinedVariable
    if u == None:
        flash('Twitter screenname not found for '+username)
        return redirect(url_for('create_name', username=username, trace=trace.serialize()))
    form = EditForm()
    if form.validate_on_submit():
        u.description = form.about_me.data
        u.last_updated = datetime.datetime.utcnow()
        db.session.add(u)
        db.session.commit()
        return redirect(url_for('user', username=user.t_screen_name, trace=trace.serialize()))
    else:
        form = EditForm()
    return render_template('user_edit_profile.html', title='Edit user '+str(username), user=u, form=form, trace=trace)

@app.route('/user/<username>')
@app.route('/user/<username>/<int:trace>')
@analyze
def user(username, trace=None):
    flash('trace: '+str(trace))
    u = User.query.filter_by(t_screen_name=username).first()  # @UndefinedVariable
    if u == None:
        flash('Twitter screenname not found for '+username)
        return redirect(url_for('create_name', username=username, trace=trace.serialize()))
    posts = u.posts.order_by(desc(Post.timestamp)).paginate(1,POSTS_PER_PAGE,False).items
    return render_template('user_profile.html', title='User '+str(username), user=u, posts=posts, trace=trace)
    
@app.route('/trace')
@app.route('/trace/<int:trace>')
@app.route('/trace/<int:trace>/<int:page>')
@analyze
def show_trace(trace=None, page=1):
    flash('trace: '+str(trace))
    # paginate
    if page <= 0:
        page = 0
        # load aggregate statistics for page
        pages = []
    else:
        pages = (PageLoad.query.filter_by(trace_id=trace.id) # @UndefinedVariable
                 .order_by(desc(PageLoad.time)) # @UndefinedVariable
                 .paginate(page,POSTS_PER_PAGE-1,False)) # @UndefinedVariable
#       posts = Post.query.order_by(Post.timestamp.desc()).paginate(page,POSTS_PER_PAGE,False) # @UndefinedVariable
    
    return render_template('trace_profile.html', title='View Trace '+str(trace.id), trace=trace, pages=pages)


@app.errorhandler(404)
@analyze
def not_found_error(error, trace=None):
    flash('trace: '+str(trace))
    return render_template('404.html', title="something wasn't found", trace=trace), 404

@app.errorhandler(500)
@analyze
def internal_server_error(error, trace=None):
    db.session.rollback()
    flash('trace: '+str(trace))
    return render_template('500.html', title="oops, the computer didn't computer", trace=trace), 500