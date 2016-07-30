from couchpotato import lazify
from nose.tools import assert_equal

def multiply(a, b):
    return a*b

def test_lazy_multiply():
    multiply_lazy = lazify(multiply)
    assert_equal(multiply(3, 4), multiply_lazy(3, 4))

