from couchpotato import lazify
from nose.tools import *

def multiply(a, b):
    return a*b

def pass_through(value):
    return value

multiply_lazy = lazify(multiply)
lazy_pass = lazify(pass_through)

def test_eq():
    print(type(lazy_pass(1)))
    print(type(pass_through(1)))
    assert_equal(lazy_pass(1), pass_through(1))

def test_not_eq():
    assert_not_equal(lazy_pass(1), pass_through(2))

def test_true():
    print(type(lazy_pass(False)))
    print(type(False))
    assert_true(lazy_pass(True))

def test_false():
    print(type(lazy_pass(False)))
    print(type(False))
    assert_false(lazy_pass(False))

def test_is_none():
    assert_is_none(lazy_pass(None))

def test_is_not_none():
    assert_is_not_none(lazy_pass(1))

def test_in():
    l = ['a', 'b', 'c']
    assert_in(lazy_pass('a'), l)

def test_not_in():
    l = ['a', 'b', 'c']
    assert_not_in(lazy_pass('d'), l)

def test_is_instance():
    assert_is_instance(lazy_pass(1), int)

def test_not_is_instance():
    assert_not_is_instance(lazy_pass('a'), int)

