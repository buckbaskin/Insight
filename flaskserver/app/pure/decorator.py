import ast
import inspect

from collections import defaultdict

class ImpureFunctionException(Exception):
    pass

class ImmutableWrapper(object):
    def __init__(self, obj):
        super(ImmutableWrapper, self).__init__()
        self.__dict__['__obj'] = obj
    def __getattr__(self, attr):
        return getattr(self.__dict__['__obj'], attr)
    def __setattr__(self, attr, val):
        raise AttributeError('object is immutable')
    def __delattr__(self, attr):
        raise AttributeError('object is immutable')

def force_immutable(obj):
    return ImmutableWrapper(obj)

class PureChecker(ast.NodeVisitor):
    def generic_visit(self, node):
        print(type(node).__name__)
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Module(self, node):
        ast.NodeVisitor.generic_visit(self, node)

    def visit_FunctionDef(self, node):
        print('this is where the action will happen')
        print('dir: '+str(node.body))
        if len(node.body) > 1:
            raise ImpureFunctionException()
        if len(node.body) == 1:
            if not isinstance(node.body[0], ast.Return) and not isinstance(node.body[0], ast.Pass):
                raise ImpureFunctionException()
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Call(self, node):
        print('this is a function call. I hope it is pure')
        print(ast.dump(node))

    def visit_Assign(self, node):
        print('assignments are not strictly speaking, okay')
        raise ImpureFunctionException()

    def visit_Global(self, node):
        print('asking to modify a global is not good')
        raise ImpureFunctionException()

def check_pure(func):
    try:
        func_source = inspect.getsource(func)
    except BaseException as e:
        print('source not available?')
        raise e

    ast_node = ast.parse(func_source)
    PureChecker().visit(ast_node)
    return func

def force_pure(func):
    func = check_pure(func)
    dict_of_args = defaultdict(dict)
    def call_replace(*args, **kwargs):
        print('begin call replace')
        # force the arguments to the function to be immutable
        new_args = (force_immutable(x) for x in args)
        new_kwargs = {n: force_immutable(kwargs[n]) for n in kwargs.keys()}
        new_kwargs = frozenset(new_kwargs)

        print('created immutable arguments')

        # memoize the function calls to force it to return the same thing
        if new_args in dict_of_args:
            if new_kwargs in dict_of_args[new_args]:
                return dict_of_args[new_args][new_kwargs]
            else:
                dict_of_args[new_args][new_kwargs] = old_call(*new_args, **dict(new_kwargs))
                return dict_of_args[new_args][new_kwargs]
        else:
            dict_of_args[new_args] = {}
            dict_of_args[new_args][new_kwargs] = old_call(*new_args, **dict(new_kwargs))
            return dict_of_args[new_args][new_kwargs]

    func.__code__ = call_replace.__code__ 
    return func
