'''
Test that each of the expected code paths functions without error. This will get
more complicated as time goes on. For tests about response time/latency
performance see test/test_app_sla.
'''
import os

from app import server as flask_app
# from Insight.service import server as flask_service
from nose.tools import ok_, assert_equal
from nose.tools import timed

app_client = None
service_client = None

def setup_module():
    global flask_app
    flask_app.config['TESTING'] = True
    if 'STATUS' not in os.environ:
        os.environ['STATUS'] = 'TESTING'
    global app_client
    app_client = flask_app.test_client()

def teardown_module():
    pass

def test_click_fail():
    res = app_client.get('/click')
    if (not res.status_code == 400):
        print(str(res.data))
    # assert_equal(400, res.status_code)

def test_click_success():
    res = app_client.get('/click?type=move&page=/jefferson&x=615&y=70&t=505620')
    if not res.status_code == 200:
        print(str(res.data))
    assert_equal(200, res.status_code)

def test_bad_format_fail():
    res = app_client.get('/click?type=move')
    assert_equal(400, res.status_code)
