class Lazily(object):
    special_names = {'__LazilyValue__', '_Lazily__evaluated', '_Lazily__func', '_Lazily__args', '_Lazily__value', '_Lazily__kwargs'}
    
    def __init__(self, func, args, kwargs):
        # print('as called __init__(%s, %s, %s)' % (func, args, kwargs,))
        self.__args = tuple(args)
        self.__kwargs = frozenset(kwargs.items())
        self.__func = func
        self.__evaluated = False
        self.__value = None

    def __LazilyValue__(self):
        if not self.__evaluated:
            print('now evaluating what the function call would be')
            print('args: %s and %s' % (self.__args, self.__kwargs,))
            self.__value = self.__func.__call__(*(self.__args), **(dict(self.__kwargs)))
            self.__evaluated = True
            print('value is now %s' % (self.__value,))

    def __str__(self):
        self.__LazilyValue__()
        return str(self.__value)
    
    def __repr__(self):
        self.__LazilyValue__()
        return repr(self.__value)

    def __setattr__(self, name, value):
        # print('__setattribute__(self, %s, %s)' % (name, value,))
        if name in Lazily.special_names:
            return object.__setattr__(self, name, value)
        self.__LazilyValue__()
        setattr(self.__value, name, value)
        
    def __getattribute__(self, name):
        # print('__getattribute__(self, %s)' % (name,))
        if name in Lazily.special_names:
            return object.__getattribute__(self, name)
        self.__LazilyValue__()
        return getattr(self.__value, name)

        # base case, if I don't do anything, just return whatever getattr should
        # return object.__getattribute__(self, name)

def lazify(func):
    def new_function(*args, **kwargs):
        # print('inside new_function: %s and %s' % (args, kwargs,))
        return Lazily(func, args, kwargs)
    new_function.__name__ = func.__name__
    return new_function

