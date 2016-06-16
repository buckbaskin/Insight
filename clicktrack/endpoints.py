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

# tasks
from Insight.sql.queues import qLow
from Insight.clicktrack.tasks import mouse_move

@server.route('/click', methods=['GET'])
@user_handler
def cursordata():
    user_id = 0
    if 'user_id' in request.cookies:
        user_id = int(request.cookies['user_id'])
    
    try:
        track_type = request.args['type']
        path = request.args['page']
        mouse_x = int(request.args['x'])
        mouse_y = int(request.args['y'])
        time = int(float(request.args['t']))
    except KeyError or ValueError:
        return make_response('Bad Request', 400)
    # send off a job request, don't care about result
    qLow.enqueue(mouse_move, user_id, path, track_type, mouse_x, mouse_y, time)
    return make_response('OK', 200)

