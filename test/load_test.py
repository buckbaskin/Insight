#! venv/bin/python3
import grequests
import itertools
from multiprocessing import Process, Queue
import numpy
import queue
import random
import time

# qps = queries per second
# qps > 0 - queries per second (uniform)
# qps < 0 - approx. queries per second (random)
# qps = 0 - no rate limit
total_qps = -10
how_many = 999
how_many_processes = 1
how_many_per_process = how_many // how_many_processes
qps = abs(float(total_qps)/how_many_processes)
del how_many
target_url = 'http://127.0.0.1:5000/index'

def uniform_yielder(iterable, rate):
    delay = 1.0/rate
    for item in iterable:
        yield item
        time.sleep(delay)

def fast_yielder(iterable, rate):
    for item in iterable:
        yield item

my_rand = random.Random(x='12345')
def random_yielder(iterable, rate):
    mean = 1.0/rate
    stdev = 0.1/rate
    delays = numpy.random.normal(mean, stdev, size=how_many_per_process)
    delays_index = 0
    for item in iterable:
        yield item
        time.sleep(delays[delays_index])
        delays_index += 1

def run(queue, how_many, time_generator, rate):
    success = 0
    urls = itertools.repeat(object=('GET', target_url,), times=how_many_per_process)
    requests = itertools.starmap(grequests.AsyncRequest, urls)
    timed_requests = time_generator(requests, rate)
    responses = grequests.imap(requests=timed_requests, size=how_many_per_process)
    
    for gg in responses:
        if (gg.status_code == 200):
            success += 1

    queue.put((success, how_many_per_process,))
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
    if total_qps == 0:
        time_generator = fast_yielder
    elif total_qps < 0:
        time_generator = random_yielder
    else:
        time_generator = uniform_yielder
    process_args = itertools.repeat(object=(None, run, None, (q, how_many_per_process, time_generator, qps,),), times=how_many_processes)

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
