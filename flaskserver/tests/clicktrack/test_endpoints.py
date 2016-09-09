'''
Test that each of the expected code paths functions without error. This will get
more complicated as time goes on. For tests about response time/latency
performance see test/test_app_sla.
'''
import json
import os
import urllib

try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote

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
    app_client.set_cookie('127.0.0.1', 'user_id', str(42))

def teardown_module():
    pass

def test_click_fail():
    # trying to get the /click endpoint should fail (endpoint not found)
    res = app_client.get('/click')
    if (not res.status_code == 404):
        print(str(res.data))
        print(str(res.status_code))
        print(str(res.headers.items()))
    assert_equal(404, res.status_code)

def test_load_success():
    data = {}
    data['page'] = '/'
    data['screen_w'] = 120
    data['screen_h'] = 120
    data['window_x'] = 0
    data['window_y'] = 0
    data['window_w'] = 120
    data['window_h'] = 120
    json_data = json.dumps(data)
    res = app_client.get('/click/l?d='+quote(str(json_data)))
    if (not res.status_code == 200):
        print(str(res.data))
        print(str(res.status_code))
        print(str(list(res.headers.items())))
    assert_equal(200, res.status_code)

def test_load_fail():
    data = {}
    data['key'] = 'value'
    json_data = json.dumps(data)
    res = app_client.get('/click/l?d='+quote(str(json_data)))
    if (not res.status_code == 400):
        print(str(res.data))
        print(str(res.status_code))
        print(str(list(res.headers.items())))
    assert_equal(400, res.status_code)

def test_mouse_success():
    data = {}
    data['page'] = '/'
    data['scroll_x'] = 0
    data['scroll_y'] = 120
    data['mouse_x'] = 0
    data['mouse_y'] = 120
    data['window_x'] = 0
    data['window_y'] = 0
    data['window_w'] = 120
    data['window_h'] = 120
    data['time'] = 9001
    json_data = json.dumps(data)
    res = app_client.get('/click/m?d='+quote(str(json_data)))
    if (not res.status_code == 200):
        print(str(res.data))
        print(str(res.status_code))
        print(str(list(res.headers.items())))
    assert_equal(200, res.status_code)

