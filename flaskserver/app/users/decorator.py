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

from flask import make_response, request, redirect, url_for
import time

def handle_user_cookie(func):
    def inner_function(*args, **kwargs):
        if 'user_id' not in request.cookies:
            new_user_id = int(time.time())
            redir = redirect(url_for('home.index'))
            response = make_response(redir)
            response.set_cookie('user_id', value=str(new_user_id))
            return response
        else:
            return make_response(func(*args, **kwargs))
    inner_function.__name__ = func.__name__
    return inner_function
