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

def setup_module():
    global flask_app
    flask_app.config['TESTING'] = True
    if 'STATUS' not in os.environ:
        os.environ['STATUS'] = 'TESTING'
    global app_client
    app_client = flask_app.test_client()
    app_client.set_cookie('127.0.0.1', 'user_id', str(42))

def teardown_module():
    pass

def test_jsload_happy():
    res = app_client.get('/performance/jsload?page=/&m=jane&resp=10&load=20')
    if (not res.status_code == 200):
        print(str(res.data))
        print(str(res.status_code))
        print(str(res.headers.items()))
    assert_equal(200, res.status_code)

def test_jsload_missing():
    res = app_client.get('/performance/jsload?page=/&m=jane')
    if (not res.status_code == 400):
        print(str(res.data))
        print(str(res.status_code))
        print(str(res.headers.items()))
    assert_equal(400, res.status_code)
