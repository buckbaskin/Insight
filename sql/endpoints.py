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
from collections import defaultdict
from rq import Queue, Worker
from rq.job import Job
from Insight.sql import r
from Insight.sql.queues import LowQ, WorkerQ
from Insight.sql.sand_funcs import calculate_factorial
from Insight.sql.worker import run_worker, kill_worker, find_and_stop

@server.route('/rq/demo/<int:number>', methods=['GET'])
@user_handler
def factorial_async(number):
    job = LowQ.enqueue(calculate_factorial, number)
    return make_response(job.id, 200)

@server.route('/rq/job/<job_id>', methods=['GET'])
@user_handler
@performance()
def check_job_status(job_id):
    job = Job.fetch(job_id, connection=r)
    if job.is_finished:
        return make_response(str(job.result), 200)
    else:
        return make_response(('Job %s not yet done.' % job_id), 202)

@server.route('/worker/add/<queue_id>')
@user_handler
@performance()
def add_worker_to_queue(queue_id):
    WorkerQ.enqueue(run_worker, [queue_id])
    return make_response('OK', 200)

@server.route('/worker/rm/<queue_id>')
@user_handler
@performance()
def remove_worker_from_queue(queue_id):
    find_and_stop(queue_id)
    return make_response('OK', 200)

@server.route('/worker')
@server.route('/worker/status')
@user_handler
@ab
@performance()
def worker_status_page(ab='A'):
    workers_dict = defaultdict(list)
    for worker in Worker.all(connection=r):
        for queue in worker.queues:
            workers_dict[queue.name].append(worker)
    queue_list = Queue.all(connection=r)
    queue_list = sorted(queue_list, key=lambda queue: queue.count, reverse=True)
    print('status for %d found' % len(queue_list))
    return render_template('worker_index.html',
                           title='Worker Status',
                           user_group=ab,
                           altJS=True,
                           queues=queue_list,
                           workers=workers_dict)

@server.route('/worker/status/<queue_id>')
@user_handler
@ab
@performance()
def queue_specific_page(queue_id, ab='A'):
    for queue_ in Queue.all(connection=r):
        if queue_.name == queue_id:
            queue = queue_
            break
    else:
        return make_response('Invalid Queue.', 400)
    workers = []
    for worker in Worker.all(connection=r):
        for queue_ in worker.queues:
            if queue_.name == queue_id:
                workers.append(worker)
                break

    return render_template('worker_queue_specific.html',
                           title='Queue '+queue_id,
                           user_group=ab,
                           altJS=True,
                           queue=queue,
                           workers=workers)
