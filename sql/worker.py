import sys
import multiprocessing

from redis import StrictRedis
from rq import Worker, Queue
from rq.worker import StopRequested
from Insight.sql import r

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
