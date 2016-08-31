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

# decorators
from Insight.abtests import ab
from Insight.automock import decorators, mock_requests
from Insight.performance import speed_test2, mem_test, performance
from Insight.users import user_handler

render_template = speed_test2()(render_template) # measure time spent rendering

# more flask
from Insight.app import server

# other
import requests
import time

@server.route('/performance/jsload', methods=['GET'])
@user_handler
def jsLoadData():
    user_id = 0
    if 'user_id' in request.cookies:
        user_id = int(request.cookies['user_id'])
    
    try:
        path = request.args['page']
        module = request.args['m']
        resp_time = int(float(request.args['resp']))
        load_time = int(float(request.args['load']))
    except KeyError or ValueError:
        return make_response('Bad Request', 400)
    print('js load: user %d on page %s, module %s response=%d load=%d' % (user_id, path, module, resp_time, load_time,))
    return make_response('OK', 200)

