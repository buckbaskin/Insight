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

from flask import request

def ab(func):
    '''
    In the future, every element in a template will have an a or b attribute,
    and then the processor will go through and select which one to use based on
    the user id. It will then track all of the experiments, and click throughs
    and such. Or something like that.
    '''
    def new_response():
        user_group = 'A'
        if 'user_id' in request.cookies:
            user_id = request.cookies['user_id']
            if int(user_id) % 2 == 1:
                user_group = 'B'

        return func(ab=user_group)
    new_response.__name__ = func.__name__
    return new_response

