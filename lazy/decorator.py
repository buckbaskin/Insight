class Lazily(object):
    def __init__(self, func, *args, **kwargs):
        print('t? %s' % (type(args)))
        self.__args = tuple(args)
        self.__kwargs = frozenset(kwargs.items())
        self.__func = func
        self.__evaluated = False
        self.__value = None

    def __LazilyValue__(self):
        if not self.__evaluated:
            print('now evaluating what the function call would be')
            self.__value = self.__func(*(self.__args), **(dict(self.__kwargs)))
            self.__evaluated = True
            print('value is now %s' % (self.__value,))

    def __str__(self):
        self.__LazilyValue__()
        return str(self.__value)
    
    def __repr__(self):
        self.__LazilyValue__()
        return repr(self.__value)

    def __setattr__(self, name, value):
        print('__setattribute__(self, %s, %s)' % (name, value,))
        object.__setattr__(self, name, value)
        
    def __getattribute__(self, name):
        print('__getattribute__(self, %s)' % (name,))
        special_names = {'__kwargs', '__args', '__value', '__func', '__evaluated', '__LazilyValue__', '__evaluated', '_Lazily__evaluated', '_Lazily__func', '_Lazily__args', '_Lazily__value', '_Lazily__kwargs'}
        if name in special_names:
            return object.__getattribute__(self, name)
        self.__LazilyValue__()
        return getattr(self.__value, name)

        # base case, if I don't do anything, just return whatever getattr should
        # return object.__getattribute__(self, name)

def my_boring_function(x, y, z):
    print('types(%s, %s)' % (type(x), type(y),))
    return x+y

def my_special_function(a, b):
    print('a '+str(a))
    # b should never get evaluated in this function
    return 10

def lazify(func):
    def new_function(*args, **kwargs):
        return Lazily(func, args, kwargs)
    new_function.__name__ = func.__name__
    return new_function

if __name__ == '__main__':
    # lazy add
    ladd = lazify(my_boring_function)
    my_special_function(ladd(1, 2), ladd(3, 4))

