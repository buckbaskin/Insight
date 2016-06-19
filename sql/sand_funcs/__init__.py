import requests

def count_words_at_url(url):
    resp = requests.get(url)
    return len(resp.text.split())

def calculate_factorial(integer):
    accum = 1
    for i in range(integer, 0, -1):
        accum *= i
    return accum

# temp use for managing workers
from rq.worker import StopRequested

def run_worker(worker):
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

def fill_time(arg):
    print(arg)
    return arg
