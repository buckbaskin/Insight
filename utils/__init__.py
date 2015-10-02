class Pluggable(object):
    def __init__(self):
        self.operations = []
    
    def add_plugin(self, f):
        self.operations.append(f)
        
    def pop_plugin(self, r):
        return self.operations.pop()
    
    def pre_call(self, *arg, **kwargs):
        pass
    
    def post_call(self, *arg, **kwargs):
        pass
    
    def run_plugins(self, *arg, **kwargs):
        for f in self.operations:
            f(arg, kwargs)
            
    def __call__(self, *arg, **kwargs):
        self.pre_call(arg)
        self.run_plugins(arg)
        self.post_call(arg)
        
class ExamplePluggablePrinter(Pluggable):
    
    def pre_call(self, *arg, **kwargs):
        super(ExamplePluggablePrinter, self).pre_call()
        print 'pre_call called'
        
    def post_call(self, *arg, **kwargs):
        super(ExamplePluggablePrinter, self).post_call()
        print 'post_call called'
        
    def plug_one(self, *arg, **kwargs):
        print 'plugin 1 called'
        
    def plug_two(self, *arg, **kwargs):
        print 'plugin 2 called'
        
def main():
    epp = ExamplePluggablePrinter()
    epp.add_plugin(epp.plug_one)
    epp.add_plugin(epp.plug_two)
    # epp()
    
    def imAFunction(*args, **kwargs):
        print 'I"m a function'
    
    p = Pluggable()
    p.add_plugin(imAFunction)
    p.add_plugin(imAFunction)
    p.add_plugin(imAFunction)
    p()
    
if __name__ == '__main__':
    main()