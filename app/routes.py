from app import server
from flask import render_template
from app import db

import analytics
import insight_apis
import task_manager

@server.route('/', methods=['GET'])
def index():
    vm = {}
    vm['title'] = 'Home'
    return render_template('index.html',
                           vm=vm)

analytic = server.route('/a', methods=['GET'])(
            server.route('/analytics', methods=['GET'])(
                 analytics.routes.a_index))
a_json = server.route('/a.json', methods=['GET'])(
             analytics.routes.a_json)

user = server.route('/u/<username>', methods=['GET'])(
       server.route('/user/<username>', methods=['GET'])(
                 insight_apis.routes.user))
u_json = server.route('/u/<username>.json', methods=['GET'])(
             insight_apis.routes.user_json)
user_process = server.route('/u/<username>/update', methods=['POST'])(
                   insight_apis.routes.update_user)

create_user = server.route('/u/new', methods=['GET'])(
              server.route('/user/new', methods=['GET'])(
                 insight_apis.routes.create_user))
c_post = server.route('/u/new', methods=['POST'])(
            insight_apis.routes.post_create)

queue = server.route('/q', methods=['GET'])(
        server.route('/queue', methods=['GET'])(
            task_manager.routes.t_index))       
q_json = server.route('/q.json')(
            task_manager.routes.t_json)

@server.errorhandler(404)
def not_found_error(error):
    return render_template('404.html', title="something wasn't found"), 404

@server.errorhandler(500)
def internal_server_error(error):
    db.session.rollback()
    return render_template('500.html', title="oops, the computer didn't computer"), 500