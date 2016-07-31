from couchpotato import lazify

def delayed_return(value):
    import time
    time.sleep(1)
    return value

def add_not_c(a, b, c):
    return a+b

if __name__ == '__main__':
    print('begin standard evaluation')
    add_not_c(1, 2, delayed_return(3))
    print('end standard evaluation')
    delayed_return = lazify(delayed_return)
    print('begin lazy evaluation')
    add_not_c(1, 2, delayed_return(3))
    print('end lazy evaluation')

