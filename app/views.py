'''
Copyright 2016 William Baskin

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''

# flask
from flask import render_template
from flask import request

# decorators
from Insight.abtests import ab
from Insight.performance import speed_test2, mem_test, performance
from Insight.users import user_handler

render_template = speed_test2()(render_template) # measure time spent rendering

# more flask
from Insight.app import server

# other
import time

@server.route('/')
@server.route('/index')
@performance
@user_handler
@ab
def index(ab='A'):
    user = {'nickname': 'Buck'}  # fake user
    posts = [
        {
            'author': {'nickname': 'John'},
            'body': 'Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'Avengers!'
        }
    ]
    user_id = 0
    if 'user_id' in request.cookies:
        user_id = request.cookies['user_id']

    return render_template('index.html',
                           title='Home',
                           user=user,
                           user_group=ab,
                           user_id=user_id,
                           posts=posts)

@server.route('/fast')
@performance
def fast():
    return "f"

@server.route('/slow')
@performance
def slow():
    time.sleep(2.0)
    return "sloooow"