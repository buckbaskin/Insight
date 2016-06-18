import redis
import rq
import subprocess

from rq import Worker

r = redis.StrictRedis(host='localhost', port=6379, db=0)

if __name__ == '__main__':
    open_process_list = {}
    while(True):
        selector = input('new or kill <id>? ')
        if selector == '':
            pass
        elif selector == 'new':
            args = ['rq', 'worker', 'userEvent', 'low']
            p = subprocess.Popen(args)
            open_process_list[p.pid] = p
            print(open_process_list)
        elif len(selector) > 4 and selector[:4] == 'new ':
            queues = selector.split(' ')
            queues = queues[1:]
            if len(queues) >= 1:
                args = ['rq', 'worker']
                args.extend(queues)
                p = subprocess.Popen(args)
                open_process_list[p.pid] = p
                print(open_process_list)
        elif len(selector) > 5 and selector[:5] == 'kill ':
# kill by id
            worker_id = selector[5:]
            worker = Worker.find_by_key(worker_id, connection=r)
            if worker is None:
                continue
            else:
                print('found kill worker: '+str(worker.key)+' with pid '+str(worker.pid))
            print(open_process_list)
            open_process_list[worker.pid].terminate()
            del open_process_list[worker.pid]
        else:
            break
        to_print = 'w { '
        for worker in Worker.all(connection=r):
            to_print += str(worker.key)+','
        to_print += ' }'
        print(to_print)
