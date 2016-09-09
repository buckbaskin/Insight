'''
Test that each of the expected code paths functions without error. This will get
more complicated as time goes on. For tests about response time/latency
performance see test/test_app_sla.
'''
import os

from app import server as flask_app
from app.performance.decorator import performance, speed_test2, mem_test
from nose.tools import ok_, assert_equal, assert_not_in, assert_in
from nose.tools import timed
from hypothesis import given
from hypothesis.strategies import text, integers, tuples, binary, one_of

global modifieds
modifieds = []

def pass_through(item):
    return item

def setup_module():
    global modifieds
    modifieds.append(performance()(pass_through))
    modifieds.append(performance('jane doe')(pass_through))
    modifieds.append(speed_test2()(pass_through))
    modifieds.append(speed_test2(logging_name='jane doe')(pass_through))
    modifieds.append(mem_test()(pass_through))

def teardown_module():
    global modifieds
    del modifieds

@given(one_of(text(), integers(), tuples(integers(), text()), binary()))
def test_performance_output(s):
    for func in modifieds:
        assert_equal(pass_through(s), func(s))

