#! venv/bin/python3
import grequests
import itertools
from multiprocessing import Process, Queue
import queue

how_many = 1000

def run(queue, how_many):
    success = 0
    urls = itertools.repeat(object=('GET', 'http://127.0.0.1:5000/index',), times=how_many)
    requests = itertools.starmap(grequests.AsyncRequest, urls)
    responses = grequests.imap(requests=requests, size=how_many)
    
    for gg in responses:
        if (gg.status_code == 200):
            success += 1

    queue.put((success, how_many,))
    print('Donezo')

def call_start(iterable):
    for x in iterable:
        x.start()
        yield x

def call_join(iterable):
    for x in iterable:
        x.join()
        yield x

if __name__ == '__main__':
    q = Queue()
    process_args = itertools.repeat(object=(None, run, None, (q, how_many,),), times=10)
    processes = itertools.starmap(Process, process_args)
    startup = call_start(processes)
#    endup = call_join(startup)
#    print(len(list(startup)))

    for object_ in startup:
        object_.join()

    requests_made = 0
    successful_requests = 0
    try:

        while True:
            result = q.get_nowait()
            requests_made += result[1]
            successful_requests += result[0]
    except queue.Empty:
        print('Success 200 %d/%d' % (requests_made, successful_requests,))
