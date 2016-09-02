'''
Test that each of the expected code paths functions without error. This will get
more complicated as time goes on. For tests about response time/latency
performance see test/test_app_sla.
'''
import os

from app import server as flask_app
from nose.tools import ok_, assert_equal
from nose.tools import timed

app_client = None
service_client = None

def setup_module():
    global flask_app, flask_service
    flask_app.config['TESTING'] = True
    if 'STATUS' not in os.environ:
        os.environ['STATUS'] = 'TESTING'
    global app_client
    app_client = flask_app.test_client()

def teardown_module():
    pass

def test_slash_redir():
    res = app_client.get('/')
    assert_equal(302, res.status_code)
    ok_(hasattr(res, 'headers'))
    assert_equal('http://127.0.0.1:5000/index', res.headers['Location'])

def test_index_success():
    res = app_client.get('/index')
    assert_equal(200, res.status_code)

def test_index_post_fail():
    res = app_client.post('/index')
    assert_equal(405, res.status_code)

def test_fast_success():
    res = app_client.get('/fast')
    assert_equal(200, res.status_code)

def test_fast_post_fail():
    res = app_client.post('/fast')
    assert_equal(405, res.status_code)

def test_slow_success():
    res = app_client.get('/slow')
    assert_equal(200, res.status_code)

def test_slow_post_fail():
    res = app_client.post('/slow')
    assert_equal(405, res.status_code)

def test_service_post_fail():
    res = app_client.post('/service')
    assert_equal(405, res.status_code)
