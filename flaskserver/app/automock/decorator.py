import os

def automock(param, default, prod=None, stage=None, test=None, dev=None):
    def inner_decorator(func): 
        def new_function(*args, **kwargs):

            # print('dec: %s,%s,%s' % (default, test, server.config['TESTING']))
            # print('dec3: prod %s stage %s test %s %s dev %s' % (prod is not None, stage is not None, test is not None, os.environ['STATUS'], dev is not None,))
            param_value = default
            if 'STATUS' in os.environ:
                if prod is not None and os.environ['STATUS'] == 'PRODUCTION':
                    print('prod case')
                    param_value = prod
                elif stage is not None and os.environ['STATUS'] == 'STAGING':
                    print('stage case')
                    param_value = stage
                elif test is not None and os.environ['STATUS'] == 'TESTING':
                    print('inside param value to tests')
                    param_value = test
                elif dev is not None and os.environ['STATUS'] == 'DEVELOPMENT':
                    print('dev case')
                    param_value = dev
                else:
                    print('default case')
                    param_value = default
            kwargs[param] = param_value
            return func(*args, **kwargs)
        new_function.__name__ = func.__name__
        return new_function
    inner_decorator.__name__ = 'automock'
    return inner_decorator

