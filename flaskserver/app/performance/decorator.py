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
import resource

def performance(logging_name=None):
    def inner_decorator(func):
        return mem_test()(
               speed_test2(logging_name, http_request=True)(
                   func
               ))
    inner_decorator.__name__ = 'performance'
    return inner_decorator

def speed_test2(logging_name=None, http_request=False):
    def wrapper_decorator(func):
        def timer_func(*args, **kwargs):
            begin = time.time()
            result = func(*args, **kwargs)
            time_taken = time.time() - begin
            if logging_name is not None:
                print('response time %f ms for %s' % (time_taken*1000, logging_name))
            else:
                print('response time %f ms for %s' % (time_taken*1000, func.__name__))
            return result
        timer_func.__name__ = func.__name__
        return timer_func
    wrapper_decorator.__name__ = 'speed_test'
    return wrapper_decorator

def mem_test():
    def wrapper_decorator(func):
        def mem_func(*args, **kwargs):
            before_mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            result = func(*args, **kwargs)
            after_mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            print('max memory usage of function: %f mb' % (max(before_mem, after_mem)/1000))
            return result
        mem_func.__name__ = func.__name__
        return mem_func
    return wrapper_decorator

# def speed_test(func):
#     def timer_func(*args, **kwargs):
#         begin = time.time()
#         result = func(*args, **kwargs)
#         print('response time for %s is %f' % (func.__name__, time.time() - begin))
#         return result
#     timer_func.__name__ = func.__name__
#     return timer_func
