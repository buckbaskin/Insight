import inspect

from web_app.app import db
# from web_app.app.models import Trace, PageLoad
# from web_app.app import models
import os
print ' *** '+str(os.getcwd())

from web_app.app.models import Trace, PageLoad

from functools import wraps

def analyze(f): # arguments to decorator
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # do stuff before function
        print '# do stuff before function'
        page_name = f.__name__
        print ' >> name = '+page_name
        parameters, _, _, defaults = inspect.getargspec(f)
        print ' >> params = '+str(parameters)
        print ' >> args   = '+str(args)
        print ' >> kwargs = '+str(kwargs)
        print ' >> defaults = '+str(defaults)
        # add page_load args to page_name
        trace = None
        if len(parameters): # if there are parameters
            for i in range(0, len(parameters)): # for each
                # print 'round '+str(i)
                if parameters[i] in kwargs: # if there is a kwarg
                    if parameters[i] is not 'trace': # and it is not trace
                        print 'param %s extended as arg %s' % (str(parameters[i]), str(kwargs[parameters[i]]))
                        page_name = page_name+'/'+str(kwargs[parameters[i]]) # add it to page_name
                    else:
                        print 'trace found as %s' % str(kwargs[parameters[i]])
                        trace = kwargs[parameters[i]]
                else:
                    # the parameter has no value
                    if parameters[i] is not 'trace': # and it is not trace
                        params_left = len(parameters)-i
                        default_index = len(defaults)-params_left
                        print 'param %s extended as def %s' % (str(parameters[i]), str(defaults[default_index]))
                        page_name = page_name+'/'+str(defaults[default_index]) # add default to page_name
                    else:
                        print 'trace found as default %s' % str(defaults[i-len(args)])
                        trace = defaults[i-len(args)]
        
        if trace is None: # create a new trace if one wasn't passed
            trace = Trace()
            # save the new trace in the db
            db.session.add(trace)
            db.session.commit()
            print 'trace created'
            if not kwargs.get('trace'):
                kwargs['trace'] = trace
            else:
                kwargs['trace'] = Trace.deserialize(kwargs['trace'])
        else:
            if isinstance(trace, int):
                kwargs['trace'] = Trace.deserialize(kwargs['trace'])
        
        # mark down the page load
        pg = PageLoad(trace=trace, page_name=page_name)
        print 'PageLoad %s created' % str(pg)
        
        # save the page data in the db
        db.session.add(pg)
        db.session.commit()
        print 'saved trace, pageload to db'
        
        print '# call function ?: %s' % page_name
        return f(*args, **kwargs)

    return decorated_function