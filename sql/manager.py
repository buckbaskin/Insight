import subprocess

from rq import Worker

if __name__ == '__main__':
    while(True):
        selector = input('new or kill <id>? ')
        if selector == 'new':
            args = ['rq', 'worker', 'userEvent', 'low']
            subprocess.Popen(args)
        elif selector[:4] == 'new ':
# create with specific queues
            pass
        elif selector[:5] == 'kill ':
# kill by id
            pass
        else:
            break
