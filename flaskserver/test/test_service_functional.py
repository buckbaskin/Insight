'''
Test that each of the expected code paths functions without error. This will get
more complicated as time goes on. For tests about response time/latency
performance see test/test_service_sla.
'''
import os

from Insight.service import server as flask_service
from nose.tools import ok_, assert_equal
from nose.tools import timed

service_client = None

def setup_module():
    global flask_service
    flask_service.config['TESTING'] = True
    if 'STATUS' not in os.environ:
        os.environ['STATUS'] = 'TESTING'
    global service_client
    service_client = flask_service.test_client()

def teardown_module():
    pass

def test_index_success():
    res = service_client.get('/data')
    assert_equal(200, res.status_code)

