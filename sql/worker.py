import sys
import multiprocessing

from redis import StrictRedis
from rq import Worker, Queue
from rq.worker import StopRequested


class StoppableWorker(Worker):

    def __init__(self, queues, connection):
        super(StoppableWorker, self).__init__(queues=queues, connection=connection)
        print('register birth?')
        self.register_birth()
        print('registed birth')

    def work(self, burst=False, logging_level="INFO"):
        self.workOnce(burst, logging_level)

    def workOnce(self, burst=False, logging_level="INFO"):
        try:
            try:
                self.check_for_suspension(burst)
                if self.should_run_maintenance_tasks:
                    self.clean_registries()

                if self._stop_requested:
                    self.log.info('Stopping on request')
                    return None

                timeout = None if burst else max(1, self.default_worker_ttl-60)

                result = self.dequeue_job_and_maintain_ttl(timeout)
                if result is None:
                    if burst:
                        self.log.info('RQ worker %s done.' % self.key)
                    return None
            except StopRequested:
                return None

            job, queue = result
            if 'kill' in job.func_name:
                print('ending '+str(self.queues)+' because of not-nice job func name')
                return False
            execute_result = self.execute_job(job, queue)
            self.heartbeat()

            did_perform_work = True
        finally:
            if not self.is_horse:
                self.register_death()
        return did_perform_work

# temp use for managing workers
from rq.worker import StopRequested

r = StrictRedis(host='localhost', port=6379, db=0)

def run_worker(qs):
    worker = StoppableWorker(qs, r)
    print('start run_worker')
    result = True
    while result is not None and result:
        print('worker loop...')
        result = worker.workOnce(burst=False)
        print('%s\n...worker loop' % (result,))
        print('this little piggy:')
        for little_worker in Worker.all(r):
            print(little_worker.key)
        print('   and that was all the little piggies')
    print('exiting working while loop :)')

def kill_worker(worker_key):
    print('kill worker %s' % worker_key)
    raise StopRequested()

def find_and_stop(queue_name):
    if queue_name == 'createWorkers':
        print('can\'t kill this little piggy')
        return 0
    for queue in Queue.all(connection=r):
        if queue.name == queue_name:
            print('I found the queueueue')
            queue.enqueue(kill_worker, 'arbitrary')
            return 1
    else:
        return 0            

def kill_gen(key):
    def killer(arg1):
        pass
    killer.func_name = 'kill'+key
    killer.__name__ = 'kill'+key
    return killer

def fill_time(arg):
    print(arg)
    return arg

