import multiprocessing

from redis import StrictRedis
from rq import Queue, Worker

from Insight.sql import r
from Insight.sql.worker import StoppableWorker
from Insight.sql.worker import run_worker, kill_worker, fill_time

workerQ = Queue('createWorkers', connection=r)
userEventQ = Queue('userEvent', connection=r)

if __name__ == '__main__':
    import time
    p = multiprocessing.Process(target=run_worker, args=(['createWorkers'],))
    p.start()
    # # have the first worker create another worker for userEvents
    # workerQ.enqueue(run_worker, ['userEvent'])

    print('this little piggy:')
    for little_worker in Worker.all(r):
        print(little_worker.key)
    print('   and that was all the little piggies')

    p.join()
    print('join :)')

    print('this little piggy:')
    for little_worker in Worker.all(r):
        print(little_worker.key)
    print('   and that was all the little piggies')

