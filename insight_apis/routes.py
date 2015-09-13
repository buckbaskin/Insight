from flask import render_template, flash, redirect, url_for, jsonify
from sqlalchemy import desc
from app.models import User, Status
from config.user_config import POSTS_PER_PAGE
from app.tasks import process_friends
from app import q

def user(username):
    vm = {}
    vm['user'] = User.query.filter_by(t_screen_name=username).first()  # @UndefinedVariable
    if vm['user'] == None:
        flash('Twitter screenname not found for '+username)
        return redirect(url_for('create_user'))
    vm['title'] = vm['user'].t_screen_name
    vm['posts'] = vm['user'].posts.order_by(desc(Status.created_at)).paginate(1,POSTS_PER_PAGE,False).items
    return render_template('user_profile.html',
                           vm=vm)
    
def user_json(username):
    u = User.query.filter_by(t_screen_name=username).first()  # @UndefinedVariable
    return jsonify(u)

def update_user(username):
    job = q.enqueue_call(
        func=process_friends, args=(username,), result_ttl=5000
    )
    return job.get_id()
    
def create_user():
    vm = {}
    vm['title'] = 'Create User'
    return render_template('user_create.html')

def post_create():
    # TODO(buckbaskin): do stuff
    return jsonify()