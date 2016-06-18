import redis
from rq import Queue

r = redis.StrictRedis(host='localhost', port=6379, db=0)
r.set('foo', 'bar')
r.get('foo')
qUserEvent = UserEventQ = Queue('userEvent', connection=r)
qLow = LowQ = Queue('low', connection=r)

del r
