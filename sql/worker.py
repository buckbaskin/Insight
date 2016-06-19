import sys
import multiprocessing

from redis import StrictRedis
from rq import Worker, Queue
from rq.worker import StopRequested

r = connection = StrictRedis(host='localhost', port=6379, db=0)

class StoppableWorker(Worker):

    def __init__(self, queues):
        super(StoppableWorker, self).__init__(queues=queues, connection=connection)
        self.register_birth()

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
            print('j>>>'+job.func_name)
            if 'kill' in job.func_name:
                print('ending because of not-nice job func name')
                return False
            execute_result = self.execute_job(job, queue)
            print('er: %s' % (execute_result,))
            self.heartbeat()

            did_perform_work = True
        finally:
            if not self.is_horse:
                self.register_death()
        return did_perform_work

# temp use for managing workers
from rq.worker import StopRequested

def run_worker(qs):
    worker = StoppableWorker(qs)
    print('start run_worker')
    result = True
    while result is not None and result:
        print('worker loop...')
        result = worker.workOnce(burst=False)
        print('%s\n...worker loop' % (result,))
    print('exiting working while loop :)')

def kill_worker(worker_key):
    print('kill worker %s' % worker_key)
    raise StopRequested()

def kill_gen(key):
    def killer(arg1):
        pass
    killer.func_name = 'kill'+key
    killer.__name__ = 'kill'+key
    return killer

def fill_time(arg):
    print(arg)
    return arg
