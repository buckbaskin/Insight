'''
Test that each of the expected code paths functions without error. This will get
more complicated as time goes on. For tests about response time/latency
performance see test/test_app_sla.
'''

import os

from Insight.app import server as flask_app
from Insight.service import server as flask_service
from nose.tools import ok_, assert_equal
from nose.tools import timed

app_client = None
service_client = None

def setup_module():
    print('Module level setup run - integration')
    flask_app.config['TESTING'] = True
    global app_client, service_client
    app_client = flask_app.test_client()
    service_client = flask_service.test_client()

def teardown_module():
    print('Module level teardown - integration')
    pass

def test_slash_redir():
    res = client.get('/')
    assert_equal(302, res.status_code)
    ok_(hasattr(res, 'headers'))
    assert_equal('http://127.0.0.1:5000/index', res.headers['Location'])

def test_index_success():
    res = client.get('/index')
    assert_equal(200, res.status_code)

def test_fast_success():
    res = client.get('/fast')
    assert_equal(200, res.status_code)

def test_slow_success():
    res = client.get('/slow')
    assert_equal(200, res.status_code)

def test_service_success():
    res = client.get('/service')
    assert_equal(200, res.status_code)

