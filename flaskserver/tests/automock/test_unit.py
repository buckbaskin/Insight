'''
Test that each of the expected code paths functions without error. This will get
more complicated as time goes on.
'''
import os

from flask import request
from app import server as flask_app
from app.automock.decorator import automock
from app.automock.mock_modules import mock_requests
from nose.tools import ok_, assert_equal, assert_not_in, assert_in
from nose.tools import timed

def setup_module():
    pass

def teardown_module():
    pass

def test_automock_outputs_function():
    def test_function(parkas):
        return parkas
    test_function = automock('parkas', 'default')(test_function)
    ok_(hasattr(test_function, '__call__'))

def test_automock_prod():
    def test_function(parkas):
        return parkas
    os.environ['STATUS'] = 'PRODUCTION'
    test_function = automock(param='parkas', default='default', prod='prod', 
                        stage='stage', test='test', dev='dev')(test_function)
    assert_equal('prod', test_function())

def test_automock_stage():
    def test_function(parkas):
        return parkas
    os.environ['STATUS'] = 'STAGING'
    test_function = automock(param='parkas', default='default', prod='prod', 
                        stage='stage', test='test', dev='dev')(test_function)
    assert_equal('stage', test_function())

def test_automock_test():
    def test_function(parkas):
        return parkas
    os.environ['STATUS'] = 'TESTING'
    test_function = automock(param='parkas', default='default', prod='prod', 
                        stage='stage', test='test', dev='dev')(test_function)
    assert_equal('test', test_function())

def test_automock_dev():
    def test_function(parkas):
        return parkas
    os.environ['STATUS'] = 'DEVELOPMENT'
    test_function = automock(param='parkas', default='default', prod='prod', 
                        stage='stage', test='test', dev='dev')(test_function)
    assert_equal('dev', test_function())

def test_automock_default():
    def test_function(parkas):
        return parkas
    os.environ['STATUS'] = 'ANYTHING_ELSE'
    test_function = automock(param='parkas', default='default', prod='prod', 
                        stage='stage', test='test', dev='dev')(test_function)
    assert_equal('default', test_function())

def test_automock_default_nostatus():
    def test_function(parkas):
        return parkas
    if 'STATUS' in os.environ:
        del os.environ['STATUS']
    assert_not_in('STATUS', os.environ)
    test_function = automock(param='parkas', default='default', prod='prod', 
                        stage='stage', test='test', dev='dev')(test_function)
    assert_equal('default', test_function())

def test_automock_requests_positive():
    print(mock_requests.get('http://127.0.0.1:5001').text)
    assert(mock_requests.get('http://127.0.0.1:5001').text == 'This is mock text')
    assert(mock_requests.get('http://127.0.0.1:5001').status_code == 200)

def test_automock_requests_negative():
    assert(mock_requests.get('something else').text == 'Default mock')
    assert(mock_requests.get('something else').status_code == 200)

