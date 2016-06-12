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
from flask import render_template, make_response
from flask import request
from werkzeug.contrib.cache import SimpleCache

# decorators
from Insight.abtests import ab
from Insight.automock import decorators, mock_requests, mock_time
from Insight.performance import speed_test2, mem_test, performance
from Insight.users import user_handler

render_template = speed_test2()(render_template) # measure time spent rendering

# more flask
from Insight.app import server

# other
import requests
import time
import jinja2

cache = SimpleCache(threshold=10, default_timeout=600)

@server.route('/', methods=['GET'])
@server.route('/index', methods=['GET'])
@performance()
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
                           posts=posts,
                           altJS=False)

@server.route('/special', methods=['GET'])
@performance()
@user_handler
@ab
def special(ab='A'):
    user = {'nickname': 'John'}
    posts = []
    user_id = 0
    if 'user_id' in request.cookies:
        user_id = request.cookies['user_id']

    return render_template('index.html',
                           title='Home',
                           user=user,
                           user_group=ab,
                           user_id=user_id,
                           posts=posts,
                           altJS=True)

@server.route('/j/<filename>.js', methods=['GET'])
@performance()
def template_js(filename):
    result = cache.get('template_js_'+filename)
    if result is None:
        print('cache miss template_js_'+filename)
        try:
            rendered = render_template('js/'+filename+'.js')
            print('saving type: %s'% type(rendered))
            cache.set('template_js_'+filename, rendered)
            return rendered
        except jinja2.exceptions.TemplateNotFound as tnf:
            print('template exception. saving as \'\'')
            cache.set('template_js_'+filename, '')
            return ''
    else:
        print('cache hit template_js_'+filename)
        return result

@server.route('/fast', methods=['GET'])
@performance()
def fast():
    return "f"

@server.route('/slow', methods=['GET'])
@performance()
@decorators.automock('time_module', default=time, test=mock_time)
def slow(time_module=time):
    time_module.sleep(2.0)
    return "sloooow"

@server.route('/service', methods=['GET'])
@performance()
@decorators.automock('requests_module', default=requests, test=mock_requests)
def service(requests_module=requests):
    requests_get = speed_test2(logging_name='requests.get')(requests_module.get)
    req_response = requests_get('http://127.0.0.1:5001/data')
    response = make_response(req_response.text, req_response.status_code)
    return response

