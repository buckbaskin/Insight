import sys
sys.path.append('/home/buck/Github/Insight')

from app import app
from flask import render_template
from app import db
from analytics import analyze

import analytics
import insight_apis
import task_manager

@app.route('/', methods=['GET'])
def index():
    vm = {}
    vm['title'] = 'Home'
    return render_template('index.html',
                           vm=vm)

analytics = app.route('/a', methods=['GET'])(
            app.route('/analytics', methods=['GET'])(
                 analytics.routes.index))
a_json = app.route('/a.json', methods=['GET'])(
             analytics.routes.json)

user = app.route('/u/<username>', methods=['GET'])(
       app.route('/user/<username>', methods=['GET'])(
                 insight_apis.routes.user))
u_json = app.route('/u/<username>.json', methods=['GET'])(
             insight_apis.routes.user_json)
user_process = app.route('/u/<username>/update', methods=['POST'])(
                   insight_apis.routes.update_user)

create_user = app.route('/u/new', methods=['GET'])(
              app.route('/user/new', methods=['GET'])(
                 insight_apis.routes.create_user))
c_post = app.route('/u/new', methods=['POST'])(
            insight_apis.routes.post_create)

queue = app.route('/q', methods=['GET'])(
        app.route('/queue', methods=['GET'])(
            task_manager.routes.index))
q_json = app.route('/q.json')(
            task_manager.routes.json)

@app.errorhandler(404)
@analyze
def not_found_error(error):
    return render_template('404.html', title="something wasn't found"), 404

@app.errorhandler(500)
@analyze
def internal_server_error(error):
    db.session.rollback()
    return render_template('500.html', title="oops, the computer didn't computer"), 500