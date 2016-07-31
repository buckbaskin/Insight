import datetime
from couchpotato import lazify

def delayed_return(value):
    import time
    time.sleep(1)
    return value

def add_not_c(a, b, c):
    return a+b

if __name__ == '__main__':
    print('standard evaluation')
    start = datetime.datetime.now()
    add_not_c(1, 2, delayed_return(3))
    delta = datetime.datetime.now() - start
    print('end standard evaluation: %s' % delta.total_seconds())
    delayed_return = lazify(delayed_return)
    print('lazy evaluation')
    start = datetime.datetime.now()
    add_not_c(1, 2, delayed_return(3))
    delta = datetime.datetime.now() - start
    print('end lazy evaluation: %s' % delta.total_seconds())

