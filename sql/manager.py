import multiprocessing

from redis import StrictRedis
from rq import Queue

from Insight.sql.worker import StoppableWorker
from Insight.sql.worker import run_worker, kill_worker, kill_gen, fill_time

r = StrictRedis(host='localhost', port=6379, db=0)
workerQ = Queue('operateWorker', connection=r)
userEventQ = Queue('userEvent', connection=r)

if __name__ == '__main__':
    import time
    print('start??')
    oneQ = Queue('1', connection=r)
    s = StoppableWorker(['1', 'userEvent'])
    
    p = multiprocessing.Process(target=run_worker, args=(s,))
    p.start()
    print('start :)')

    oneQ.enqueue(kill_worker, s.key)

    print('join??')
    p.join()
    print('join :)')

