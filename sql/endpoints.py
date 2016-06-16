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
import redis
from rq.job import Job
from Insight.sql.queues import qLow
from Insight.sql.sand_funcs import calculate_factorial

conn = redis.StrictRedis(host='localhost', port=6379, db=0)

@server.route('/rq/demo/<int:number>', methods=['GET'])
@user_handler
def factorial_async(number):
    job = qLow.enqueue(calculate_factorial, number)
    return make_response(job.id, 200)

@server.route('/rq/job/<job_id>', methods=['GET'])
@user_handler
@performance()
def check_job_status(job_id):
    job = Job.fetch(job_id, connection=conn)
    if job.is_finished:
        return make_response(str(job.result), 200)
    else:
        return make_response(('Job %s not yet done.' % job_id), 202)

