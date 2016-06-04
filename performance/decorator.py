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

import time

def speed_test2():
    def wrapper_decorator(func):
        def timer_func(*args, **kwargs):
            begin = time.time()
            result = func(*args, **kwargs)
            print('response time %f sec for %s' % (time.time() - begin, func.__name__))
            return result
        timer_func.__name__ = func.__name__
        return timer_func
    wrapper_decorator.__name__ = 'speed_test'
    return wrapper_decorator

def speed_test(func):
    def timer_func(*args, **kwargs):
        begin = time.time()
        result = func(*args, **kwargs)
        print('response time for %s is %f' % (func.__name__, time.time() - begin))
        return result
    timer_func.__name__ = func.__name__
    return timer_func