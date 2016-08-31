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
from Insight.sql.queues import TwitterLimitedQ
from Insight.twitter_api.tasks import get_followers_test, screen_name_to_id

@server.route('/twitter/demo', methods=['GET'])
@user_handler
def twitter_example():
    job = TwitterLimitedQ.enqueue(get_followers_test, screen_name_to_id('beBaskin'))
    return make_response(job.id, 200)

