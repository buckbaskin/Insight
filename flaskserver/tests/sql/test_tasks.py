'''
Test the functionality of each of the sql/tasks
'''
import os

from nose.tools import ok_, assert_equal, assert_not_in, assert_in
from nose.tools import raises
from app.sql import tasks
from rq.worker import StopRequested

def setup_module():
    pass

def teardown_module():
    pass

@raises(StopRequested)
def test_stop_raises_error():
    tasks.kill_worker('Worker Key')
