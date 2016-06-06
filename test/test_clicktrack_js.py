'''
Test the javascript functions that are being run on the client side
'''
import execjs
import os

from Insight.app import server as flask_app
from Insight.service import server as flask_service
from nose.tools import ok_, assert_equal, assert_is_not_none
from nose.tools import timed

ctx = None
node = None

def setup_module():
    global node, ctx
    node = execjs.get(execjs.runtime_names.Node)
    clickjs_file = open('app/static/click.js')
    ctx = node.compile(clickjs_file)

def teardown_module():
    pass

@timed(.1)
def test_click_compile():
    assert_is_not_none(ctx)
    assert_equal(200, 200)

