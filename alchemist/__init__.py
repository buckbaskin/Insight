import os

def lead(gold):
    print('gold: %s' % gold)
    def object_replacer(obj):
        print('lead: %s' % obj)
        try:
            if os.environ['STATUS'] == 'TESTING':
                print('lead to testing gold')
                return gold
        finally:
            print('no status, choose lead.')
            return obj
    return object_replacer
