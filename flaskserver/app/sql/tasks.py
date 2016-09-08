from rq import Queue, Worker
from rq.worker import StopRequested
from app.sql import r
from app.sql.worker import StoppableWorker

def run_worker(qs):
    worker = StoppableWorker(qs, r)
    print('start run_worker')
    result = True
    while result is not None and result:
        # print('worker loop...')
        result = worker.workOnce(burst=False)
        # print('%s\n...worker loop' % (result,))
        # print('this little piggy:')
        # for little_worker in Worker.all(r):
        #     print(little_worker.key)
        # print('   and that was all the little piggies')
    print('exiting working while loop :)')

def kill_worker(worker_key):
    print('kill worker %s' % worker_key)
    raise StopRequested()

def find_and_stop(queue_name):
    if queue_name == 'createWorkers':
        print('can\'t kill all the little piggies')
        count_of_creators = 0
        for worker in Worker.all(connection=r):
            for queue in worker.queues:
                if queue.name == 'createWorkers':
                    count_of_creators += 1

        if count_of_creators == 0:
            return 0

    for queue in Queue.all(connection=r):
        if queue.name == queue_name:
            print('I found the queueueue')
            queue.enqueue(kill_worker, 'arbitrary')
            return 1
    else:
        return 0            

# def kill_gen(key):
#     def killer(arg1):
#         pass
#     killer.func_name = 'kill'+key
#     killer.__name__ = 'kill'+key
#     return killer
