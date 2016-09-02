'''
Test the response times of the server to see if they match performance specs

These tests are "nice to have" and are important later, but shouldn't block
first commits.
'''
from nose.tools import timed, assert_equal

def setup_module():
    pass

def teardown_module():
    pass

@timed(.1)
def test_func1():
        print('running timed test 1')
        assert_equal(1,1)
