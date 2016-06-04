import os

from Insight.app import server as flask_app
from nose.tools import assert_equal
from nose.tools import timed

client = None

def setup_module():
    print('Module level setup run - integration')
    flask_app.config['TESTING'] = True
    client = flask_app.test_client()

@timed(.1)
def test_func1():
    print('running test 1')
    assert_equal(1,1)

def teardown_module():
    print('Module level teardown - integration')
    pass
