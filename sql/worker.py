import sys
import multiprocessing

from redis import StrictRedis
from rq import Worker, Queue
from rq.worker import StopRequested

r = connection = StrictRedis(host='localhost', port=6379, db=0)
workerQ = Queue('operateWorker', connection=r)
userEventQ = Queue('userEvent', connection=r)

from Insight.sql.sand_funcs import run_worker, kill_worker, fill_time

class StoppableWorker(Worker):

    def __init__(self, queues):
        super(StoppableWorker, self).__init__(queues=queues, connection=connection)

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
            execute_result = self.execute_job(job, queue)
            print('er: %s' % (execute_result,))
            self.heartbeat()

            did_perform_work = True
        finally:
            if not self.is_horse:
                self.register_death()
        return result

if __name__ == '__main__':
    import time
    print('start??')
    oneQ = Queue('1', connection=r)
    s = StoppableWorker(['1', 'operateWorker', 'userEvent'])
    
    p = multiprocessing.Process(target=run_worker, args=(s,))
    p.start()
    print('start :)')

    time.sleep(5)

    userEventQ.enqueue(fill_time, 1)
    oneQ.enqueue(kill_worker, s.key)
    userEventQ.enqueue(fill_time, 1)
    userEventQ.enqueue(fill_time, 1)

    print('join??')
    p.join()
    print('join :)')

