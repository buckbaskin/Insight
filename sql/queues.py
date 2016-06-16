import redis
from rq import Queue

r = redis.StrictRedis(host='localhost', port=6379, db=0)
r.set('foo', 'bar')
r.get('foo')
qLow  = Queue('low', connection=r)

del r
