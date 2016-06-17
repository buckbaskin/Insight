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
        path = request.args['page']
        screen_x = int(request.args['sx'])
        screen_y = int(request.args['sy'])
        window_x = int(request.args['wx'])
        window_y = int(request.args['wy'])
    except KeyError or ValueError:
        return make_response('Bad Request', 400)
    qLow.enqueue(page_load, user_id, path, 'load', screen_x, screen_y, 
                 window_x, window_y)
    return make_response('OK', 200)


@server.route('/click/m', methods=['GET'])
@user_handler
def cursordata():
    user_id = 0
    if 'user_id' in request.cookies:
        user_id = int(request.cookies['user_id'])
    
    try:
        track_type = request.args['type']
        path = request.args['page']
        scroll_x = int(request.args['sx'])
        scroll_y = int(request.args['sy'])
        mouse_x = int(request.args['mx'])
        mouse_y = int(request.args['my'])
        time = int(float(request.args['t']))
    except KeyError or ValueError:
        return make_response('Bad Request', 400)
    # send off a job request, don't care about result
    qLow.enqueue(mouse_move, user_id, path, track_type, scroll_x, scroll_y, 
                 mouse_x, mouse_y, time)
    return make_response('OK', 200)

