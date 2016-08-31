import redis
from Insight.sql import r
from rq import Queue

r.set('foo', 'bar')
r.get('foo')
qTwitterLimited = TwitterLimitedQ = Queue('twitter:Limited', connection=r)
qUserEvent = UserEventQ = Queue('userEvent', connection=r)
qLow = LowQ = Queue('low', connection=r)
qWorker = WorkerQ = Queue('createWorkers', connection=r)

del r
