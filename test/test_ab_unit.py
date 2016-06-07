'''
Test that each of the expected code paths functions without error. This will get
more complicated as time goes on. For tests about response time/latency
performance see test/test_app_sla.
'''
import os

from flask import request
from Insight.app import server as flask_app
from Insight.abtests.decorator import ab
from nose.tools import ok_, assert_equal, assert_not_in, assert_in
from nose.tools import timed

def setup_module():
    pass

def teardown_module():
    pass

def test_ab_outputs_function():
    with flask_app.test_request_context('/'):
        mod_cookies = dict(request.cookies)
        mod_cookies['user_id'] = 5
        request.cookies = mod_cookies
        assert_in('user_id', request.cookies)
        def test_function(ab='SpallingJackRabbit'):
            return ab
        test_function = ab(test_function)
        ok_(hasattr(test_function, '__call__'))

def test_ab_assigns_b_odd():
    with flask_app.test_request_context('/'):
        mod_cookies = dict(request.cookies)
        mod_cookies['user_id'] = 5
        request.cookies = mod_cookies
        assert_in('user_id', request.cookies)
        def test_function(ab='SpallingJackRabbit'):
            return ab
        test_function = ab(test_function)
        assert_equal('B', test_function()) 
def test_ab_assigns_a_empty():
    with flask_app.test_request_context('/'):
        mod_cookies = dict(request.cookies)
        request.cookies = mod_cookies
        assert_not_in('user_id', request.cookies)
        def test_function(ab='SpallingJackRabbit'):
            return ab
        test_function = ab(test_function)
        assert_equal('A', test_function())

def test_ab_assigns_a_even():
    with flask_app.test_request_context('/'):
        mod_cookies = dict(request.cookies)
        mod_cookies['user_id'] = 4
        request.cookies = mod_cookies
        assert_in('user_id', request.cookies)
        def test_function(ab='SpallingJackRabbit'):
            return ab
        test_function = ab(test_function)
        assert_equal('A', test_function())

def test_ab_overwrite_not_supported():
    with flask_app.test_request_context('/'):
        def test_function(cd='lala'):
            return cd
        test_function = ab(test_function)
        assert_equal('lala', test_function())
