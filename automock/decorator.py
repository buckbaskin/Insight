from Insight.app import server

def automock(param, default, prod=None, stage=None, test=None, dev=None):
    def inner_decorator(func): 
        if prod is not None:
           param_value = prod
        elif stage is not None:
           param_value = stage
        elif test is not None and server.config['TESTING']:
           param_value = test
        elif dev is not None:
           param_value = dev
        else:
           param_value = default
        def new_function(*args, **kwargs):
            kwargs[param] = param_value
            return func(*args, **kwargs)
        new_function.__name__ = func.__name__
        return new_function
    inner_decorator.__name__ = 'automock'
    return inner_decorator

