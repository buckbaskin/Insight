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
    with open('app/static/small.js', 'r') as clickjs_file:
        code = ''.join([str(line) for line in clickjs_file])
        ctx = node.compile(code)

def teardown_module():
    pass

@timed(.1)
def test_small_compile():
    assert_is_not_none(ctx)
    document = 1
    window = 2
    xhr = 3
    debug = True
    assert_is_not_none(ctx.call('test_this', 1, 2))
    assert_equal(200, 200)

