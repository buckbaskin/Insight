import os
import sys
if not '/home/buck/Github/Insight' in sys.path:
    sys.path.append('/home/buck/Github/Insight')
print 'redis_worker.py: '
print sys.path

import redis
from rq import Worker, Queue, Connection

listen = ['default']

redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')

conn = redis.from_url(redis_url)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()