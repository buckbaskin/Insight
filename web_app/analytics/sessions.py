import inspect

from web_app.app import db
from web_app.app.models import Session, PageLoad

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
        # add page_load args to page_name
        ses = None
        if len(parameters): # if there are parameters
            for i in range(0, len(parameters)): # for each
                # print 'round '+str(i)
                if len(args) > i: # if there is an arg
                    if parameters[i] is not 'session': # and it is not session
                        print 'param %s extended as arg %s' % (str(parameters[i]), str(args[i]))
                        page_name = page_name+'/'+str(args[i]) # add it to page_name
                    else:
                        print 'session found as %s' % str(args[i])
                        ses = args[i]
                else:
                    if parameters[i] is not 'session': # and it is not session
                        print 'param %s extended as def %s' % (str(parameters[i]), str(defaults[i-len(args)]))
                        page_name = page_name+'/'+str(defaults[i-len(args)]) # add default to page_name
                    else:
                        print 'session found as default %s' % str(defaults[i-len(args)])
                        ses = defaults[i-len(args)]
        
        if ses is None: # create a new session if one wasn't passed
            ses = Session()
            # save the new session in the db
            db.session.add(ses)
            db.session.commit()
            print 'session created'
            if not kwargs.get('session'):
                kwargs['session'] = ses
            else:
                kwargs['session'] = Session.deserialize(kwargs['session'])
        
        # mark down the page load
        pg = PageLoad(session=ses, page_name=page_name)
        print 'PageLoad %s created' % str(pg)
        
        # save the page data in the db
        db.session.add(pg)
        db.session.commit()
        print 'saved sesssion, pageload to db'
        
        print '# call function ?: %s' % page_name
        return f(*args, **kwargs)

    return decorated_function