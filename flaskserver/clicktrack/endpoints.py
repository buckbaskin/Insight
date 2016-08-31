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
import json
import requests
import time

# tasks
from Insight.sql.queues import UserEventQ
from Insight.clicktrack.tasks import mouse_move, page_load

@server.route('/click/l', methods=['GET'])
@user_handler
def pageloaddata():
    '''
    One time message for every page load that tells info about the page.
    This will be the first information used to render the page as the user
    saw it.
    '''
    user_id = 0
    if 'user_id' in request.cookies:
        user_id = int(request.cookies['user_id'])

    try:
        json_data = request.args['d']
        data = json.loads(json_data)
        path = data['page']
        screen_w = data['screen_w']
        screen_h = data['screen_h']
        window_x = data['window_x']
        window_y = data['window_y']
        window_w = data['window_w']
        window_h = data['window_h']
    except KeyError or ValueError:
        return make_response('Bad Request', 400)
    UserEventQ.enqueue(page_load, user_id, path, screen_w, screen_h,
                       window_x, window_y, window_w, window_h)
    return make_response('OK', 200)


@server.route('/click/m', methods=['GET'])
@user_handler
def cursordata():
    user_id = 0
    if 'user_id' in request.cookies:
        user_id = int(request.cookies['user_id'])
    
    try:
        data = json.loads(request.args['d'])
        path = data['page']
        window_x = data['window_x']
        window_y = data['window_y']
        window_w = data['window_w']
        window_h = data['window_h']
        scroll_x = data['scroll_x']
        scroll_y = data['scroll_y']
        mouse_x = data['mouse_x']
        mouse_y = data['mouse_y']
        time = data['time']
    except KeyError or ValueError:
        return make_response('Bad Request', 400)
    # send off a job request, don't care about result
    UserEventQ.enqueue(mouse_move, user_id, path, scroll_x, scroll_y, 
                 mouse_x, mouse_y, time)
    return make_response('OK?', 200)

