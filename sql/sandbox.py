#! venv/bin/python3

from Insight.sql.sand_funcs import count_words_at_url

import redis
from rq import Queue

r = redis.StrictRedis(host='localhost', port='6379', db=0)
q_low = Queue('low', connection=r)

print('%d jobs waiting on queue \'low\' at time of submit')
job = q_low.enqueue(count_words_at_url, 'http://nvie.com')
print(job.result)

import time

time.sleep(2)
print(job.result)
